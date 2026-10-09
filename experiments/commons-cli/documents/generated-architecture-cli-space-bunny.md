# Apache Commons CLI

## Overview

Apache Commons CLI is a Java library (Maven artifact `commons-cli`, version `1.12.0-SNAPSHOT`, targeting Java 8) for parsing command-line arguments and rendering usage/help text. It is a pure library with no entry point or `main` method: applications declare a set of `Options`, hand them plus a `String[]` of arguments to a `CommandLineParser`, and query the resulting `CommandLine`. The codebase is split into two packages: `org.apache.commons.cli` (model, parsing, conversion) and `org.apache.commons.cli.help` (a pluggable help/rendering layer added in 1.10.0).

## Components

### Option Model

- **Purpose** — Declarative description of what a command line accepts, and the container that holds those descriptions.
- **Key source locations** — `Option.java`, `Options.java`, `OptionGroup.java`, `OptionValidator.java`, `DeprecatedAttributes.java`, `Char.java`
- **Interactions** — `Option.Builder` (nested in `Option`) is the sole modern construction path; it delegates short-name validation to `OptionValidator.validate`. `Options.addOption(Option)` indexes each option into two `LinkedHashMap`s keyed by `Option.getKey()` (short name, falling back to long name) and by long name, and records required options in a `requiredOpts` list. `Options.addOptionGroup(OptionGroup)` force-clears `required` on every member option (`Options.java:158`) and registers the group in an `optionGroups` map, so requirement is enforced at the group level. `OptionGroup.setSelected(Option)` enforces mutual exclusion and throws `AlreadySelectedException`. The `help` package reads this model read-only: `AbstractHelpFormatter` sorts options and asks `Options.getOptionGroup(Option)` to recover grouping for syntax rendering.

### DefaultParser (current parser)

- **Purpose** — Single-pass parser that converts raw argument tokens into a `CommandLine`.
- **Key source locations** — `DefaultParser.java`, `CommandLineParser.java`, `ParseException.java` and subclasses
- **Interactions** — Reads exclusively from an `Options` instance via `hasOption`/`hasShortOption`/`hasLongOption`/`getOption`/`getMatchingOptions`. Writes results into a `CommandLine` built by `CommandLine.builder()`, and mutates `OptionGroup` selection state through `updateRequiredOptions(Option)`. Constant prefixes (`-`, `--`, `=`) come from `org.apache.commons.cli.help.OptionFormatter.DEFAULT_OPT_PREFIX`, so parsing and help rendering share one source of truth for token syntax.

### Legacy Parser Hierarchy

- **Purpose** — Deprecated two-pass parsers retained for backward compatibility.
- **Key source locations** — `Parser.java`, `BasicParser.java`, `GnuParser.java`, `PosixParser.java`
- **Interactions** — `Parser` is an abstract `CommandLineParser` whose template method `parse(...)` calls the subclass hook `flatten(Options, String[], boolean)` to normalize arguments into a flat token array, then walks those tokens with a `ListIterator` in `processOption`/`processArgs`. `BasicParser.flatten` echoes arguments unchanged; `GnuParser.flatten` splits `--opt=value` and `-Dkey=value` forms; `PosixParser.flatten` additionally bursts concatenated short options (`-abc`) via `burstToken`. They reuse `DefaultParser.indexOfEqual` (package-private static) for `=` location. `OptionBuilder` (deprecated, explicitly documented as not thread-safe) and `PatternOptionBuilder` are the matching legacy construction APIs.

### Type Conversion

- **Purpose** — Convert raw `String` option values into typed objects on demand.
- **Key source locations** — `Converter.java`, `TypeHandler.java`
- **Interactions** — `TypeHandler` holds a `Class -> Converter` map built by `createDefaultMap()` covering primitives, `BigInteger`/`BigDecimal`, `File`, `Path`, `URL`, `Class`, `FileInputStream`, and `Date`; unknown types fall back to the identity `Converter.DEFAULT`. Conversion is lazy — `Option.getConverter()` delegates to the singleton `TypeHandler.getDefault()`, and `CommandLine.getParsedOptionValue(...)` / `getParsedOptionValues(...)` invoke it, wrapping any failure via `ParseException.wrap`. `PatternOptionBuilder.build(Options)` builds a per-call `TypeHandler` seeded from `createDefaultMap()`.

### CommandLine (Result)

- **Purpose** — Immutable-ish query object over the parse result: which options were seen, their values, and leftover non-option arguments.
- **Key source locations** — `CommandLine.java`, `Option.java` (value storage)
- **Interactions** — Holds a `List<Option>` of *processed copies* plus a `LinkedList<String>` of leftover args. `resolveOption(String)` strips leading hyphens and linearly scans the processed list matching `getOpt()`/`getLongOpt()`. Values themselves live on the `Option` instances, not here. Deprecated-option warnings are emitted lazily on access via the injected `Consumer<Option> deprecatedHandler` (default writes to `System.out`), which is propagated from `DefaultParser.Builder.setDeprecatedHandler`.

### Help Rendering (`org.apache.commons.cli.help`)

- **Purpose** — Format options into usage lines and tables, with output format chosen by the caller.
- **Key source locations** — `AbstractHelpFormatter.java`, `HelpFormatter.java`, `OptionFormatter.java`, `HelpAppendable.java`, `FilterHelpAppendable.java`, `TextHelpAppendable.java`, `TableDefinition.java`, `TextStyle.java`, `Util.java`
- **Interactions** — A three-layer split: (1) `AbstractHelpFormatter` composes output by calling `HelpAppendable.appendParagraph/appendTable/appendHeader`; (2) `HelpAppendable` is a semantic `Appendable` interface (paragraph vs. title vs. table), implemented by `TextHelpAppendable` (plain text, wraps at `maxWidth` and auto-fits table columns via `adjustTableFormat`) and by `FilterHelpAppendable`, a pass-through base that forwards raw `Appendable` calls to an underlying sink and is subclassed for alternate formats (`AptHelpAppendable`, `XhtmlHelpAppendable` in tests); (3) `TableDefinition` + `TextStyle` carry column widths, alignment, indentation and `scalable` flags used during table fitting. `help.HelpFormatter.getTableDefinition` builds the standard `Options | Since | Description` table from per-option `OptionFormatter`s; `OptionFormatter` (in `help`, distinct from the deprecated `cli.HelpFormatter`) owns all syntax-string details — opt prefixes, separators, `<arg>` and `[optional]` delimiters, and user-supplied format functions.

## Data / Control Flow

Parsing (`DefaultParser.parse(options, properties, nonOptionAction, arguments...)`):

1. Reset state: `expectedOpts` seeded from `options.getRequiredOptions()`, every `OptionGroup.setSelected(null)`.
2. For each argument, `handleToken(token)` dispatches in this order:
   - if `skipParsing` (set by a previous `--`), append as a plain arg;
   - if token is exactly `--`, set `skipParsing = true`;
   - if an option is currently awaiting a value and `isArgument(token)` holds (i.e. not an option, or a negative number via `isNegativeNumber`), attach the value via `Option.processValue`;
   - if token starts with `--` → `handleLongOption` (with/without `=`), resolving through `getMatchingLongOptions` for partial matching, throwing `AmbiguousOptionException` on >1 match;
   - if token starts with `-` → `handleShortAndLongOption`, which tries short option, partial long match, long-prefix (`-Xmx512m`), Java-property (`-Dkey=value`), then `handleConcatenatedOptions` bursting;
   - otherwise → `handleUnknownToken(token)`, governed by `NonOptionAction` (`IGNORE`/`SKIP`/`STOP`/`THROW`).
3. `handleOption` clones the `Option` (so accumulated values are per-occurrence), calls `updateRequiredOptions` (removes it from `expectedOpts`, marks its group selected — throwing `AlreadySelectedException` if a sibling was already chosen), and appends the clone to the `CommandLine`.
4. After the loop: `checkRequiredArgs()` (throws `MissingArgumentException`), `handleProperties(properties)` (applies defaults, skipping options already present or in a selected group), then `checkRequiredOptions()` (throws `MissingOptionException` with the remaining list).

Help rendering (`AbstractHelpFormatter.printHelp(cmdLineSyntax, header, options, footer, autoUsage)`):

1. Emit `"usage: " + syntax` — appending `toSyntaxOptions(options)` only when `autoUsage` is set. `toSyntaxOptions` sorts options, renders each `OptionGroup` once via `toSyntaxOptions(OptionGroup)` joined by `" | "` and wrapped in `[...]` when optional, and renders standalone options via `OptionFormatter.toSyntaxOption()`.
2. Emit the optional header paragraph.
3. Delegate to the abstract `getTableDefinition(Iterable<Option>)`; `help.HelpFormatter` implements it as a 3-column table.
4. `TextHelpAppendable.appendTable` recomputes column max widths from headers and cells, shrinks *scalable* columns proportionally when the total exceeds `maxWidth`, converts each cell to a `Queue<String>` of wrapped lines, and interleaves them row-wise.
5. Emit the optional footer paragraph.

## Key Decisions & Gotchas

- **Two coexisting parser designs.** `DefaultParser` is single-pass and stateful (mutable `cmd`, `currentOption`, `skipParsing`, `expectedOpts` fields); the deprecated `Parser` base is two-pass (`flatten` then iterate). They share almost no code except the static `DefaultParser.indexOfEqual`. `DefaultParser` instances are therefore **not thread-safe / not reusable concurrently**, and `OptionBuilder` carries an explicit not-thread-safe warning for CLI-209.
- **Cloning per occurrence.** Every matched option is `clone()`d before being added to the `CommandLine`, so repeated flags (`-v -v -v`) accumulate as separate entries and `CommandLine.getOptionCount(String)` counts them. The legacy `Parser.parse` explicitly calls `Option.clearValues()` on all options first (CLI-71) because it mutates the shared `Options`; `DefaultParser` avoids that via cloning.
- **`Options` mutability leaks into `Option`.** `Options.addOptionGroup` calls `option.setRequired(false)` on its members, so adding an option to a group permanently mutates the caller's `Option`. `Option.getKey()` prefers the short name and falls back to the long name, which is why `Options` can key both maps consistently.
- **`requiredOpts` is a heterogeneous list.** Both `Options` and `DefaultParser` keep required expectations in a raw `List<Object>` mixing `String` keys and `OptionGroup` instances (both files carry a `// TODO this seems wrong` comment) — required-option tracking is untyped at runtime.
- **Three-valued quote handling.** `stripLeadingAndTrailingQuotes` is a `Boolean` where `null` means legacy behavior: strip for space-separated values (`stripLeadingAndTrailingQuotesDefaultOn`) but not for attached/equals-separated ones (`...DefaultOff`). Quotes are only stripped when the outermost pair is balanced and the interior contains no quote (`Util.stripLeadingAndTrailingQuotes`).
- **Partial long-option matching is global and can surprise.** `Options.getMatchingOptions` prefix-matches every long option name, so `-de` can resolve to `debug` or throw `AmbiguousOptionException` depending on what else is registered; `DefaultParser.Builder.setAllowPartialMatching(false)` restricts it to exact matches.
- **Deprecated-option warnings fire on read, not on parse.** `CommandLine.handleDeprecated` is invoked from `hasOption`/`getOptionValues`, so a warning prints each time the option is queried; the handler is a transient field and defaults to `System.out`. `Option.converter` and `DeprecatedAttributes` are `transient`, so serialization falls back to the default `TypeHandler` map.
- **Rendering constants are shared with the parser.** `-`, `--`, `=`, `, `, `usage: `, and the default `<arg>` / `[optional]` delimiters live as constants on `help.OptionFormatter` and are referenced from `DefaultParser`, `Parser`, `PosixParser`, `OptionGroup`, and `cli.Util`. Any help-format customization therefore has parse-side implications.
- **`Converter.DATE` is deliberately strict and locale-aware.** It disables lenient parsing, rejects trailing garbage by requiring full consumption of a `ParsePosition`, and retries with `Locale.ENGLISH` when the default locale matches nothing — so `"Feb 30"` and `"<valid date> garbage"` are rejected rather than rolled over or truncated.
- **`AbstractHelpFormatter` requires non-null collaborators.** Its constructor `Objects.requireNonNull`s the appendable, option-formatter builder, and comparator; the builder setters substitute defaults for `null` rather than rejecting. Its `toSyntaxOptions(Iterable<Option>)` overload cannot see groups, so the `Options`/`OptionGroup` overloads must be used when grouping matters.