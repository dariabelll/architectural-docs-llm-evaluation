# Documentation Evaluation

## Metadata

| Field | Value |
|---|---|
| Repository | `/Users/dariabelll/Desktop/docs-llm-proj-test/commons-cli` |
| Source commit | `d95484f57dfa4b99ac9069bb3f44df680306e8e9` |
| Candidate document | `/Users/dariabelll/Desktop/docs-llm-proj-test/commons-cli/generated-architecture-cli-space-bunny.md` |
| Candidate SHA-256 | `9275c0030d04ef5260d665eb753185ea302178cd149bf60be0b846b1ae2e162c` |
| Reference facts | `/Users/dariabelll/Desktop/docs-llm-proj-test/commons-cli/reference-facts.md` (frozen set created earlier in this session, used unchanged) |
| Reference SHA-256 | `51aaec37fa3842be4a7986707bd0d90227722f13207a735a192d9ea52af16878` |
| Generating model | Space Bunny Free (`space-bunny-free`) — per the filename `…-space-bunny` |
| Evaluating model | Space Bunny Free (`space-bunny-free`) — self-evaluation |
| Evaluation date | 2026-10-09 |
| Evidence base | `src/main/java/org/apache/commons/cli/**`, `src/test/java/org/apache/commons/cli/**`, `pom.xml`. No README/site/xdoc/AGENTS/CHANGELOG content used as evidence. |

**Note.** The same frozen reference set (SHA-256 `51aaec37…`) is used for both candidates, so precision and recall are directly comparable. The reference file was verified byte-identical before this evaluation. Note that this candidate is self-evaluated (same model for generation and verification), which the metrics below reflect.

---

## Precision

Independently verifiable factual claims extracted from the candidate and checked against source. Compound sentences were split rather than judged as a whole.

### Overview

| Claim | Verdict | Evidence |
|---|---|---|
| P-01 Maven artifact `commons-cli`, version `1.12.0-SNAPSHOT` | Supported | `pom.xml:24-32` |
| P-02 Targeting Java 8 | Supported | `pom.xml:89-90` |
| P-03 Pure library with no entry point or `main` method | Supported | No `public static void main` under `src/main/java/`; library build |
| P-04 Applications declare `Options`, hand them plus a `String[]` to a `CommandLineParser`, and query the resulting `CommandLine` | Supported | `CommandLineParser.java:24-34`, `CommandLine.java:963-1013` |
| P-05 The codebase is split into `org.apache.commons.cli` and `org.apache.commons.cli.help` | Supported | `src/main/java/org/apache/commons/cli/`, `.../help/` |
| P-06 The help/rendering layer was added in 1.10.0 | Supported | `help/AbstractHelpFormatter.java:37`, `help/HelpFormatter.java:60`, `help/package-info.java:31` |

### Component: Option model

| Claim | Verdict | Evidence |
|---|---|---|
| P-07 `Option.Builder` (nested in `Option`) is the **sole modern** construction path | **Unsupported** | Evidence contradicts the claim: `Option` also exposes three public constructors that are **not** deprecated — `Option(String, boolean, String)` (`Option.java:465`), `Option(String, String)` (`Option.java:476`), `Option(String, String, boolean, String)` (`Option.java:489`). The only `@Deprecated` members of `Option` are `Builder.build()` (`:134`), `addValue()` (`:533`) and `setType(Object)` (`:969`). |
| P-08 `Option.Builder` delegates short-name validation to `OptionValidator.validate` | Supported | `Option.java:259-262`, `Option.java:112-114` |
| P-09 `Options.addOption(Option)` indexes each option into two `LinkedHashMap`s keyed by `Option.getKey()` and by long name | Supported | `Options.java:48`, `Options.java:51`, `Options.java:74-89` (`shortOpts.put(opt.getKey(), opt)`, `longOpts.put(opt.getLongOpt(), opt)`) |
| P-10 …and records required options in a `requiredOpts` list | Supported | `Options.java:56`, `Options.java:81-86` |
| P-11 `Options.addOptionGroup` force-clears `required` on every member option (`Options.java:158`) | Supported | `Options.java:158` — `option.setRequired(false);` (cited line is exact) |
| P-12 …and registers the group in an `optionGroups` map, so requirement is enforced at the group level | Supported | `Options.java:150-165`, `Options.java:151-153` |
| P-13 `OptionGroup.setSelected(Option)` enforces mutual exclusion and throws `AlreadySelectedException` | Supported | `OptionGroup.java:134-147` |
| P-14 The help package reads the model read-only; `AbstractHelpFormatter` sorts options and asks `Options.getOptionGroup(Option)` to recover grouping | Supported | `AbstractHelpFormatter.java:391-408`, `:442-472`, `:506-508` |

### Component: `DefaultParser`

| Claim | Verdict | Evidence |
|---|---|---|
| P-15 Reads exclusively from an `Options` instance via `hasOption`/`hasShortOption`/`hasLongOption`/`getOption`/`getMatchingOptions` | Supported | `DefaultParser.java:307`, `:351`, `:370`, `:396`, `:400`, `:451`, `:468`, `:474`, `:538`, `:546`, `:559`, `:573`, `:659`, `:674`, `:721-725` |
| P-16 Writes results into a `CommandLine` built by `CommandLine.builder()` | Supported | `DefaultParser.java:750` |
| P-17 Mutates `OptionGroup` selection state through `updateRequiredOptions(Option)` | Supported | `DefaultParser.java:846-858`, called at `:482` |
| P-18 Prefix constants `-` and `--` come from `help.OptionFormatter.DEFAULT_OPT_PREFIX` / `DEFAULT_LONG_OPT_PREFIX` | Supported | `DefaultParser.java:28`, `:605`, `:611`; `OptionFormatter.java:279`, `:284` |
| P-19 …as does the `=` constant | **Unsupported** | Evidence contradicts the claim: `=` is **not** an `OptionFormatter` constant. `DefaultParser.indexOfEqual` uses `Char.EQUAL` (`DefaultParser.java:190`), defined in the package-private `Char.java:28`. `OptionFormatter` defines only `-`, `--`, `", "`, `" "`, `"usage: "`, `"arg"`, `[`, `]`, `<`, `>` (`OptionFormatter.java:229-294`). |
| P-20 Parsing and help rendering therefore share one source of truth for token syntax | Supported | Shared constants across `DefaultParser.java:605,611`, `Parser.java:169-178`, `PosixParser.java:145-146`, `OptionGroup.java:162-166`, `Util.java:79-84` |

### Component: legacy parser hierarchy

| Claim | Verdict | Evidence |
|---|---|---|
| P-21 `Parser` is an abstract `CommandLineParser` whose template method `parse(...)` calls the subclass hook `flatten(Options, String[], boolean)` | Supported | `Parser.java:35`, `:74`, `:103-105`, `:119-121`, `:162` |
| P-22 …then walks those tokens with a `ListIterator` in `processOption`/`processArgs` | Supported | `Parser.java:163`, `:184`, `:247-263`, `:217-237` |
| P-23 `BasicParser.flatten` echoes arguments unchanged | Supported | `BasicParser.java:50-56` |
| P-24 `GnuParser.flatten` splits `--opt=value` and `-Dkey=value` forms | Supported | `GnuParser.java:68-78` |
| P-25 `PosixParser.flatten` additionally bursts concatenated short options via `burstToken` | Supported | `PosixParser.java:86`, `:179` |
| P-26 The legacy parsers reuse `DefaultParser.indexOfEqual` (package-private static) for `=` location | Supported | `GnuParser.java:68`, `PosixParser.java:150`; `DefaultParser.java:189-191`. (`BasicParser.flatten` is a pure echo and does not use it.) |
| P-27 `OptionBuilder` (deprecated, explicitly documented as not thread-safe) and `PatternOptionBuilder` are the matching legacy construction APIs | Supported | `OptionBuilder.java:29`, `:32`; `PatternOptionBuilder.java:80` |

### Component: type conversion

| Claim | Verdict | Evidence |
|---|---|---|
| P-28 `TypeHandler` holds a `Class -> Converter` map built by `createDefaultMap()` covering `BigInteger`/`BigDecimal`, `File`, `Path`, `URL`, `Class`, `FileInputStream` and `Date` | Supported | `TypeHandler.java:80-82`, `:221-249` |
| P-29 …covering **primitives** | **Unsupported** | Evidence contradicts the claim: the map contains **no** primitive `Class` keys (no `int.class`, `double.class`, …). It registers the wrappers `Long`, `Integer`, `Short`, `Byte`, `Character`, `Double`, `Float` (`TypeHandler.java:229-247`). `Option.type` is likewise declared `Class<?>`, never a primitive type (`Option.java:314-317`, `:956-958`). |
| P-30 Unknown types fall back to the identity `Converter.DEFAULT` | Supported | `TypeHandler.java:290-292`, `Converter.java:41` |
| P-31 Conversion is lazy — `Option.getConverter()` delegates to the singleton `TypeHandler.getDefault()` | Supported | `Option.java:610-612`, `TypeHandler.java:45`, `:203-205` |
| P-32 `CommandLine.getParsedOptionValue(...)` / `getParsedOptionValues(...)` invoke it, wrapping any failure via `ParseException.wrap` | Supported | `CommandLine.java:620-623`, `:814-818` |
| P-33 `PatternOptionBuilder.build(Options)` builds a per-call `TypeHandler` | **Unsupported** | Evidence contradicts the claim: `PatternOptionBuilder` has **no** `build` method. Its public API is `getValueClass(char)`, `getValueType(char)`, `isValueCode(char)`, `parsePattern(String)` and the constructor (`PatternOptionBuilder.java:121`, `:132`, `:163`, `:173`, `:236`). The per-call `TypeHandler` is created inside `parsePattern` (`PatternOptionBuilder.java:210-213`). |
| P-34 …seeded from `createDefaultMap()` | Supported | `PatternOptionBuilder.java:210` — `TypeHandler.createDefaultMap()` |

### Component: `CommandLine`

| Claim | Verdict | Evidence |
|---|---|---|
| P-35 "Immutable-ish" query object over the parse result | **Unsupported** | Evidence contradicts the claim: `CommandLine` has protected mutators — `addArg(String)` (`CommandLine.java:185`) and `addOption(Option)` (`:196`) — and exposes its live collections: `getArgList()` returns the internal `args` list itself (`:221-223`) and `iterator()` returns a live iterator (`:1011-1013`). Its final fields hold mutable `LinkedList`/`ArrayList` instances (`CommandLine.java:56`, `:59`). |
| P-36 Holds a `List<Option>` of *processed copies* plus a `LinkedList<String>` of leftover args | Supported | `CommandLine.java:56`, `:59`, `:481-483` (clones) |
| P-37 `resolveOption(String)` strips leading hyphens and linearly scans the processed list matching `getOpt()`/`getLongOpt()` | Supported | `CommandLine.java:1035-1043` |
| P-38 Values themselves live on the `Option` instances, not in `CommandLine` | Supported | `CommandLine.java:511`, `:531`, `:807` |
| P-39 Deprecated-option warnings are emitted lazily on access via the injected `Consumer<Option> deprecatedHandler` (default writes to `System.out`) | Supported | `CommandLine.java:53`, `:933-937` |
| P-40 …which is propagated from `DefaultParser.Builder.setDeprecatedHandler` | Supported | `DefaultParser.java:128-131`, `:750` |

### Component: help rendering

| Claim | Verdict | Evidence |
|---|---|---|
| P-41 `AbstractHelpFormatter` composes output by calling `HelpAppendable.appendParagraph`/`appendTable`/`appendHeader` | Supported | `AbstractHelpFormatter.java:333-343` |
| P-42 `HelpAppendable` is a semantic `Appendable` interface (paragraph vs. title vs. table) | Supported | `HelpAppendable.java:24-37`, `:68-120` |
| P-43 …implemented by `TextHelpAppendable` (plain text, wraps at `maxWidth`, auto-fits table columns via `adjustTableFormat`) | Supported | `TextHelpAppendable.java:35`, `:362-393`, `:152-200`, `:243-254` |
| P-44 …and by `FilterHelpAppendable`, a pass-through base that forwards raw `Appendable` calls to an underlying sink and is subclassed for alternate formats (`AptHelpAppendable`, `XhtmlHelpAppendable` in tests) | Supported | `FilterHelpAppendable.java:38-72`; `src/test/java/org/apache/commons/cli/example/AptHelpAppendable.java:34`, `.../XhtmlHelpAppendable.java:32` |
| P-45 `TableDefinition` + `TextStyle` carry column widths, alignment, indentation and `scalable` flags used during table fitting | Supported | `TableDefinition.java:36-101`, `TextStyle.java:28`, `:284-331`, `TextHelpAppendable.java:152-200` |
| P-46 `help.HelpFormatter.getTableDefinition` builds the standard `Options \| Since \| Description` table from per-option `OptionFormatter`s | Supported | `HelpFormatter.java:163-208`, labels at `:107`, `:112`, `:117` |
| P-47 `OptionFormatter` (in `help`, distinct from the deprecated `cli.HelpFormatter`) owns all syntax-string details — opt prefixes, separators, `<arg>` and `[optional]` delimiters, and user-supplied format functions | Supported | `OptionFormatter.java:32`, `:228-294`, `:112-215` |

### Data / control flow — parsing

| Claim | Verdict | Evidence |
|---|---|---|
| P-48 Reset state: `expectedOpts` seeded from `options.getRequiredOptions()`, every `OptionGroup.setSelected(null)` | Supported | `DefaultParser.java:745`, `:747-749` |
| P-49 If `skipParsing` (set by a previous `--`), append as a plain arg | Supported | `DefaultParser.java:603-604` |
| P-50 If the token is exactly `--`, set `skipParsing = true` | Supported | `DefaultParser.java:605-606` |
| P-51 If an option is awaiting a value and `isArgument(token)` holds (not an option, or a negative number via `isNegativeNumber`), attach via `Option.processValue` | Supported | `DefaultParser.java:607-608`, `:648-650`, `:690-697` |
| P-52 If the token starts with `--` → `handleLongOption` (with/without `=`), resolving through `getMatchingLongOptions`, throwing `AmbiguousOptionException` on >1 match | Supported | `DefaultParser.java:609-610`, `:418-424`, `:365-374`, `:442-443`, `:470-471` |
| P-53 If it starts with `-` → `handleShortAndLongOption`, trying short option, partial long match, long-prefix (`-Xmx512m`), Java-property (`-Dkey=value`), then `handleConcatenatedOptions` bursting | Supported | `DefaultParser.java:611-612`, `:533-592`, `:393-407` |
| P-54 Otherwise → `handleUnknownToken(token)`, governed by `NonOptionAction` | Supported | `DefaultParser.java:613-615`, `:630-641`, `:159-177` |
| P-55 `handleOption` clones the `Option` (so accumulated values are per-occurrence), calls `updateRequiredOptions` (removes it from `expectedOpts`, marks its group selected — throwing `AlreadySelectedException` if a sibling was already chosen), and appends the clone | Supported | `DefaultParser.java:478-485`, `:846-858`, `OptionGroup.java:143-145`, `Option.java:556-565` |
| P-56 `checkRequiredArgs()` throws `MissingArgumentException` | Supported | `DefaultParser.java:319-326`, `MissingArgumentException.java:23-39` |
| P-57 `handleProperties(properties)` applies defaults, skipping options already present or in a selected group | Supported | `DefaultParser.java:492-520` (`:505`) |
| P-58 `checkRequiredOptions()` throws `MissingOptionException` with the remaining list | Supported | `DefaultParser.java:333-338`, `MissingOptionException.java:25-51` |

### Data / control flow — help rendering

| Claim | Verdict | Evidence |
|---|---|---|
| P-59 Emit `"usage: " + syntax`, appending `toSyntaxOptions(options)` only when `autoUsage` is set | Supported | `AbstractHelpFormatter.java:332-336`, `:180` |
| P-60 `toSyntaxOptions` sorts options, renders each `OptionGroup` once joined by `" | "`, wrapped in `[...]` when optional, and renders standalone options via `OptionFormatter.toSyntaxOption()` | Supported | `AbstractHelpFormatter.java:442-472`, `:480-498`, `:175`, `:467` |
| P-61 Emit the optional header paragraph | Supported | `AbstractHelpFormatter.java:337-339` |
| P-62 Delegate to the abstract `getTableDefinition(Iterable<Option>)`; `help.HelpFormatter` implements it as a 3-column table | Supported | `AbstractHelpFormatter.java:340`, `:285`, `help/HelpFormatter.java:163-208` |
| P-63 `TextHelpAppendable.appendTable` recomputes column max widths from headers and cells, shrinks *scalable* columns proportionally when the total exceeds `maxWidth`, converts each cell to a `Queue<String>` of wrapped lines, and interleaves them row-wise | Supported | `TextHelpAppendable.java:243-254`, `:152-200`, `:336-360`, `:445-465` |
| P-64 Emit the optional footer paragraph | Supported | `AbstractHelpFormatter.java:341-343` |

### Key decisions & gotchas

| Claim | Verdict | Evidence |
|---|---|---|
| P-65 `DefaultParser` is single-pass and stateful (mutable `cmd`, `currentOption`, `skipParsing`, `expectedOpts`) | Supported | `DefaultParser.java:194`, `:219`, `:222`, `:227`; `:751-755` (no `flatten` phase) |
| P-66 The deprecated `Parser` base is two-pass (`flatten` then iterate) | Supported | `Parser.java:162-203` |
| P-67 They share almost no code except the static `DefaultParser.indexOfEqual` | Supported | Neither class extends the other (`Parser.java:35`, `DefaultParser.java:35`); the only cross-reference between the two families is `GnuParser.java:68` and `PosixParser.java:150` calling `DefaultParser.indexOfEqual` |
| P-68 `DefaultParser` instances are not thread-safe / not reusable concurrently | Supported | Mutable instance parse state (`DefaultParser.java:194-227`) with no synchronization anywhere in `src/main/java` |
| P-69 `OptionBuilder` carries an explicit not-thread-safe warning for CLI-209 | Supported | `OptionBuilder.java:29` |
| P-70 Every matched option is `clone()`d before being added, so repeated flags (`-v -v -v`) accumulate as separate entries and `CommandLine.getOptionCount(String)` counts them | Supported | `DefaultParser.java:481-483`, `CommandLine.java:263-265`, `:241-254` |
| P-71 The legacy `Parser.parse` explicitly calls `Option.clearValues()` on all options first (CLI-71) | Supported | `Parser.java:152-153` — `options.helpOptions().forEach(Option::clearValues);` with the CLI-71 comment |
| P-72 …*because it mutates the shared `Options`* | **Unsupported** | Evidence contradicts the stated rationale: the in-code rationale is re-use across parses — "clear out the data in options in case it's been used before (CLI-71)" (`Parser.java:152`) and "After a parse is complete, these are left with data in them and they need clearing if another parse is done" (`Option.java:538-542`). The clone-based mechanism exists precisely so option *values* are never shared with the `Options` registry. |
| P-73 `DefaultParser` avoids that via cloning | Supported | `DefaultParser.java:481`; no `clearValues` call in `DefaultParser.parse` (`:739-762`) |
| P-74 `Options.addOptionGroup` calls `option.setRequired(false)`, so grouping permanently mutates the caller's `Option` | Supported | `Options.java:154-163` |
| P-75 `Option.getKey()` prefers the short name and falls back to the long name | Supported | `Option.java:648-651` |
| P-76 …which is why `Options` can key both maps consistently | Supported | `Options.java:75`, `:87` (short map keyed by `getKey()`), `:78` (long map keyed by `getLongOpt()`) |
| P-77 Both `Options` and `DefaultParser` keep required expectations in a raw `List<Object>` | **Unsupported** | Half-contradicted: `Options.requiredOpts` **is** `List<Object>` (`Options.java:56`), but `DefaultParser.expectedOpts` is a **raw `List`**, not `List<Object>` (`DefaultParser.java:227`) — the same distinction missed by the MiMo candidate, here stated the other way round. |
| P-78 Both files carry a `// TODO this seems wrong` comment | Supported | `Options.java:55`, `DefaultParser.java:226` |
| P-79 Required-option tracking is untyped at runtime | Supported | Raw/heterogeneous containers (`Options.java:56`, `DefaultParser.java:227`), untyped `expectedOpts.remove(option.getKey())` (`DefaultParser.java:848`) |
| P-80 `stripLeadingAndTrailingQuotes` is a `Boolean` where `null` means legacy: strip for space-separated values (`...DefaultOn`) but not for attached/equals-separated ones (`...DefaultOff`) | Supported | `DefaultParser.java:61`, `:148-151`, `:821-839` |
| P-81 Quotes are only stripped when the outermost pair is balanced and the interior contains no quote | Supported | `Util.java:58-67` |
| P-82 `Options.getMatchingOptions` prefix-matches every long option name, so `-de` can resolve to `debug` or throw `AmbiguousOptionException` | Supported | `Options.java:220-232`; the `-de`/`debug` example is the library's own (`DefaultParser.java:98-110`, `:248-260`); ambiguity at `:442-443` |
| P-83 `DefaultParser.Builder.setAllowPartialMatching(false)` restricts it to exact matches | Supported | `DefaultParser.java:116-119`, `:365-374` |
| P-84 `CommandLine.handleDeprecated` is invoked from `hasOption`/`getOptionValues`, so a warning prints **each time** the option is queried | Supported | `CommandLine.java:933-937`, `:976-979`, `:508-510`; no memoization |
| P-85 The handler is a `transient` field and defaults to `System.out` | Supported | `CommandLine.java:162`, `:53` |
| P-86 `Option.converter` and `Option.deprecated` (`DeprecatedAttributes`) are `transient` fields | Supported | `Option.java:396`, `:404` |
| P-87 …so after deserialization `converter` falls back to the default `TypeHandler` map | Supported | `Option.java:610-612`, `TypeHandler.java:203-205` |
| P-88 `-`, `--`, `", "`, `"usage: "`, `"arg"` and the `[`/`]` (and `<`/`>`) delimiters live as constants on `help.OptionFormatter` | Supported | `OptionFormatter.java:279`, `:284`, `:289`, `:274`, `:237`, `:229`, `:232` |
| P-89 …as does the `=` constant | **Unsupported** | Evidence contradicts the claim — see P-19: `=` is `Char.EQUAL` (`Char.java:28`), referenced at `DefaultParser.java:190`, `GnuParser.java:75-76`, `OptionBuilder.java:307`, `Option.java:325` |
| P-90 These constants are referenced from `DefaultParser`, `Parser`, `PosixParser`, `OptionGroup` and `cli.Util` | Supported | `DefaultParser.java:28`, `Parser.java:27`, `PosixParser.java:25`, `OptionGroup.java:26`, `Util.java:20` |
| P-91 "Any help-format customization therefore has parse-side implications" | **Unsupported** | Evidence contradicts the claim: presentation is customized through `OptionFormatter.Builder` instance setters (`setOptPrefix`, `setLongOptPrefix`, `setOptSeparator`, `setOptArgSeparator`, `setOptionalDelimiters` — `OptionFormatter.java:153-204`), which are consumed only by `AbstractHelpFormatter.getOptionFormatBuilder().build(option)` (`help/HelpFormatter.java:183`, `AbstractHelpFormatter.java:248-250`). The parsers read the **static** `OptionFormatter.DEFAULT_*` fields directly (`DefaultParser.java:605`, `:611`), so builder-level customization never reaches the parse side. |
| P-92 `Converter.DATE` disables lenient parsing | Supported | `Converter.java:74-75` (`format.setLenient(false)`) |
| P-93 It rejects trailing garbage by requiring full consumption of a `ParsePosition` | Supported | `Converter.java:79-93` |
| P-94 It retries with `Locale.ENGLISH` when the default locale matches nothing, so `"Feb 30"` and `"<valid date> garbage"` are rejected rather than rolled over or truncated | Supported | `Converter.java:77-94` (`non-lenient` rejects out-of-range fields; `pos.getIndex() != s.length()` rejects trailing text) |
| P-95 `AbstractHelpFormatter`'s constructor `Objects.requireNonNull`s the appendable, option-formatter builder and comparator | Supported | `AbstractHelpFormatter.java:209-212` |
| P-96 "the builder setters substitute defaults for `null` rather than rejecting" | **Unsupported** | Evidence contradicts the blanket claim: only two setters substitute — `setHelpAppendable` (`:138-140`) and `setOptionFormatBuilder` (`:149-151`). `setComparator` assigns the argument directly with no null handling (`:127-130`), so a `null` comparator reaches the constructor's `requireNonNull` and throws. `setOptionGroupSeparator` uses a different mechanism (`Util.defaultValue`, `:161`). |
| P-97 `AbstractHelpFormatter.toSyntaxOptions(Iterable<Option>)` cannot see groups | Supported | `AbstractHelpFormatter.java:431-433` (`o -> null` lookup) and the javadoc at `:421-426` |
| P-98 …so the `Options`/`OptionGroup` overloads must be used when grouping matters | Supported | `AbstractHelpFormatter.java:506-508`, `:480-498` |

**Supported claims: 88**
**Total claims: 98**

---

## Recall

Reference set: the same frozen 88 architectural facts (`reference-facts.md`, SHA-256 `51aaec37…`), unchanged from the MiMo evaluation.

| Reference fact | Covered | Evidence |
|---|---|---|
| RF-01 Single-module Maven project | Yes | Candidate line 5 |
| RF-02 Coordinates + parent `commons-parent:105` | Yes | Candidate line 5; parent at `pom.xml:27-31` |
| RF-03 Java 8 source/target | Yes | Candidate line 5; `pom.xml:89-90` |
| RF-04 No compile/runtime dependencies; all test-scoped | No | The candidate calls it a "pure library" (line 5) but never discusses dependencies |
| RF-05 36 main / 51 test Java files | No | Not mentioned |
| RF-06 Two production packages | Yes | Candidate line 5 |
| RF-07 `help` names four user-facing types | Yes | Candidate lines 41-43 names all four; `help/package-info.java:19-30` |
| RF-08 `cli.Util`/`cli.Char` package-private helpers; separate package-private `help.Util` | No | All three files are named (lines 12, 42, 77) but only `cli.Util` has a stated interaction (line 77); no characterization of any as package-private internal helpers — name mentions only |
| RF-09 `Option` is `Cloneable, Serializable` with the full attribute set | No | `Option`'s attributes (argCount, argName, `type`, `optionalArg`, `since`, `valueSeparator`, `values`) are never enumerated; `Cloneable`/`Serializable` never mentioned (`Option.java:41`, `:390-431`) |
| RF-10 `UNINITIALIZED = -1` / `UNLIMITED_VALUES = -2` semantics | No | Not mentioned |
| RF-11 `Option` built via nested `Builder`, validated by `OptionValidator.validate` | Yes | Candidate line 13 |
| RF-12 `hasArg()`/`hasArgs()`/`acceptsArg()`/`requiresArg()` semantics | No | Not described (`Option.java:507-509`, `:755-775`, `:878-883`) |
| RF-13 `processValue` splits on `valueSeparator` | No | `processValue` is named (lines 53, 57) but its splitting rule is not (`Option.java:844-871`) |
| RF-14 `clone()` duplicates the values list → per-occurrence values | Yes | Candidate lines 57, 71 ("accumulated values are per-occurrence"); `Option.java:556-565` |
| RF-15 `clearValues()` empties values between parses (CLI-71) | Yes | Candidate line 71 — and here attributed correctly to the legacy `Parser` only |
| RF-16 `getKey()` = short else long; identifier for required tracking and grouping | Yes | Candidate lines 13, 72, 75; `Option.java:648-651` |
| RF-17 `getConverter()` falls back to `TypeHandler.getDefault().getConverter(type)` | Yes | Candidate line 31; `Option.java:610-612` |
| RF-18 `getValues()` returns `null` when empty | No | Not mentioned |
| RF-19 `OptionValidator` character rules (`?`/`@` first, `-` later) | No | Named only (line 13); `OptionValidator.java:28-31`, `:122-145` uncovered |
| RF-20 `OptionGroup` internals (ordered map, `selected`, `required`) | No | Name + one method only (line 13); `OptionGroup.java:39-45` uncovered |
| RF-21 `setSelected` throws `AlreadySelectedException` | Yes | Candidate lines 13, 57; `OptionGroup.java:134-147` |
| RF-22 `Options` registry with the four collections | Yes | Candidate line 13 (two maps, `requiredOpts` list, `optionGroups` map); `Options.java:48-59` |
| RF-23 `addOption` registers in `longOpts`/`shortOpts` and `requiredOpts` | Yes | Candidate line 13; `Options.java:74-89` |
| RF-24 `addOptionGroup` forces optional, removes from `requiredOpts`, maps key→group | Yes | Candidate lines 13, 72; `Options.java:150-165` |
| RF-25 Lookups normalise via `stripLeadingHyphens`, short map first | Yes | Candidate lines 13, 37 |
| RF-26 `getMatchingOptions` prefix/partial matching | Yes | Candidate lines 54, 75; `Options.java:220-232` |
| RF-27 `getRequiredOptions`/`getOptionGroups` (HashSet dedup)/`getOptions` semantics | No | Not mentioned (`Options.java:264-289`, `:330-332`) |
| RF-28 `addOptions` duplicate-key `IllegalArgumentException` | No | Not mentioned (`Options.java:175-184`) |
| RF-29 Fluent `Options` API | No | Not mentioned |
| RF-30 `CommandLineParser` SPI with both overloads | Yes | Candidate lines 5, 18 |
| RF-31 `DefaultParser` single-pass; `Parser` deprecated two-pass | Yes | Candidate lines 17, 23, 70 |
| RF-32 `DefaultParser` configurable state via `builder()` | Yes | Candidate lines 37, 70, 74, 75; `DefaultParser.java:47-152` |
| RF-33 `NonOptionAction` enum; boolean overloads delegate to STOP/THROW | Yes | Candidate lines 56, 70 |
| RF-34 Canonical `parse(...)` entry point and sequence | Yes | Candidate lines 47-58 |
| RF-35 `handleToken` dispatch order | Yes | Candidate lines 50-56 enumerate the same branches in the same order |
| RF-36 `handleShortAndLongOption` token forms | Yes | Candidate line 55 |
| RF-37 `getLongPrefix` prefix scanning | No | Candidate line 55 names `-Xmx512m` but not the scanning mechanism (`DefaultParser.java:345-357`) |
| RF-38 Ambiguous partial matches → `AmbiguousOptionException` | Yes | Candidate lines 54, 75 |
| RF-39 `handleUnknownToken` throws only on THROW; STOP sets `skipParsing` | No | Candidate line 56 says only "governed by `NonOptionAction`"; the throw/STOP semantics are not stated |
| RF-40 `isArgument` = not an option or a negative number | Yes | Candidate line 53; `DefaultParser.java:648-650` |
| RF-41 Tri-state quote stripping with DefaultOn/DefaultOff | Yes | Candidate line 74 |
| RF-42 Every occurrence cloned; clone becomes `currentOption` | Yes | Candidate lines 57, 71; `DefaultParser.java:478-485` |
| RF-43 `checkRequiredArgs` throws `MissingArgumentException` | Yes | Candidate line 58; the `-Dflag` exemption (`DefaultParser.java:321-323`) is a missing detail, not the core fact |
| RF-44 `updateRequiredOptions` removes key/group, marks selection | Yes | Candidate line 57 |
| RF-45 `handleProperties` full rules (unknown key throws, `yes`/`true`/`1`) | No | Candidate line 58 covers only the skipping rule (`DefaultParser.java:505`); `:499-501` and `:512-514` uncovered |
| RF-46 Deprecated `Parser` two-pass loop details | No | Candidate line 25 covers `flatten` + iteration, not the `--`/`-`/`stopAtNonOption` handling (`Parser.java:162-203`) |
| RF-47 `Parser.parse` full reset (values, group selections, required snapshot) | No | Candidate line 71 covers `clearValues` only; group-selection clearing and `setOptions` (`Parser.java:155-157`, `:311-314`) not attributed to `Parser` |
| RF-48 `BasicParser`/`GnuParser`/`PosixParser` `flatten` behaviours | Yes | Candidate line 25 — echo, `--opt=value`/`-Dkey=value` splitting, `burstToken` bursting |
| RF-49 `Parser.processOption` behaviour | No | Not described (`Parser.java:247-263`) |
| RF-50 `CommandLine` internals (LinkedList args, ArrayList of clones, transient handler) | Yes | Candidate lines 36, 37, 76 |
| RF-51 `resolveOption` strips hyphens, matches `getOpt()`/`getLongOpt()` | Yes | Candidate line 37 |
| RF-52 Value-lookup API surface | Yes | Candidate lines 28, 35, 37, 71 establish `hasOption`, `getOptionValue(s)`, `getParsedOptionValue(s)`, `getOptionCount`, leftover args; `getOptionProperties`/`iterator`/`getArgs` omitted but the query responsibility is covered |
| RF-53 Typed access via `getConverter()` + `ParseException.wrap` | Yes | Candidate line 31 |
| RF-54 Deprecation warnings lazy on query, default to `System.out` | Yes | Candidate lines 37, 76 |
| RF-55 `getOptionProperties` pairing rule; `getOptionValue(OptionGroup)` | No | Not mentioned (`CommandLine.java:1023-1027`, `:422-424`) |
| RF-56 `Converter<T,E>` interface and its predefined converters | No | Only `Converter.DEFAULT` is named (line 31); the interface and `CLASS`/`FILE`/`PATH`/`NUMBER`/`OBJECT`/`URL`/`DATE` constants are not covered (`Converter.java:34-108`) |
| RF-57 `TypeHandler` map, singleton `getDefault()`, `Converter.DEFAULT` fallback | Yes | Candidate line 31; `TypeHandler.java:45`, `:203-205`, `:290-292` |
| RF-58 `TypeHandler` static helpers deprecated / `createFiles` unimplemented | No | Candidate line 31 names `ParseException.wrap` but neither the deprecated statics nor the unimplemented ones (`TypeHandler.java:106-218`) |
| RF-59 `DeprecatedAttributes` immutable value object with `Builder` | No | Named as a key source location (line 12) and as a `transient` field (line 76); its `description`/`since`/`forRemoval` content is never described |
| RF-60 `OptionBuilder` static-state, not thread safe (CLI-209) | Yes | Candidate lines 25, 70 |
| RF-61 `PatternOptionBuilder.parsePattern` value codes and `!` | No | Candidate lines 25, 31 name the class; no value codes, no `!`, no unsupported `File[]` converter (`PatternOptionBuilder.java:132-156`, `:210-214`) |
| RF-62 `ParseException` checked + `wrap` semantics | No | Line 31 mentions `ParseException.wrap` exists; the checked nature and the wrap semantics (return-if-`ParseException`, rethrow `UnsupportedOperationException`) are not covered (`ParseException.java:23`, `:44-52`) |
| RF-63 `ParseException` subtype taxonomy | Yes | Candidate lines 18, 55, 57, 58 |
| RF-64 `AmbiguousOptionException extends UnrecognizedOptionException` | No | Candidate line 18 lists the exceptions flatly as "ParseException.java and subclasses"; the intermediate parent is not established (`AmbiguousOptionException.java:28`) |
| RF-65 `HelpAppendable` output SPI with semantic operations | Yes | Candidate line 43 |
| RF-66 `FilterHelpAppendable` delegation contract and role | Yes | Candidate line 43 |
| RF-67 `TextHelpAppendable` wrapping, table fitting, constants | Yes | Candidate lines 43, 65 |
| RF-68 `TableDefinition` immutable table description | Yes | Candidate line 43; `TableDefinition.java:36-101` |
| RF-69 `TextStyle` immutable style with alignment/indent/width/scalable | Yes | Candidate lines 43, 65 |
| RF-70 `OptionFormatter` defaults | Yes | Candidate lines 43, 77 enumerate the prefixes, separators, `arg`, `<>` and `[]`; `OptionFormatter.java:229-294` |
| RF-71 `OptionFormatter` accessors | No | Not listed (`OptionFormatter.java:384-480`) |
| RF-72 `AbstractHelpFormatter` framework + self-typed `Builder` | Yes | Candidate lines 41, 43, 79; `AbstractHelpFormatter.java:33-38`, `:51-213` |
| RF-73 `printHelp` composition | Yes | Candidate lines 60-66 cover usage, header, table, footer; the `IllegalArgumentException` on empty syntax (`AbstractHelpFormatter.java:329-331`) is a missing detail |
| RF-74 `toSyntaxOptions` group handling, separator, optional wrapping | Yes | Candidate line 62 |
| RF-75 `help.HelpFormatter` 3-column table with `Since` column | Yes | Candidate lines 43, 64 |
| RF-76 Format-agnostic plug points | Yes | Candidate lines 41, 43 ("output format chosen by the caller", subclasses for alternate formats) |
| RF-77 Legacy `HelpFormatter` deprecated and independent (`PrintWriter`, no help-subsystem use) | No | Candidate line 43 only notes it is "distinct from the deprecated `cli.HelpFormatter`"; the `PrintWriter`-based independent renderer (`HelpFormatter.java:73-74`, `:326`) is not described |
| RF-78 Legacy formatter's mutable state and method set | No | Not mentioned (`HelpFormatter.java:545-995`) |
| RF-79 One-way constant aliasing (`cli.HelpFormatter` → `help.OptionFormatter`) | No | Not mentioned (`HelpFormatter.java:206-209`) |
| RF-80 Definition flow | Yes | Candidate lines 5, 13 |
| RF-81 Modern parse flow end to end | Yes | Candidate lines 47-58 |
| RF-82 Legacy parse flow | Yes | Candidate line 25 |
| RF-83 Help flow | Yes | Candidate lines 60-66 |
| RF-84 Typed value flow | Yes | Candidate line 31 |
| RF-85 Error flow — `ParseException` subtypes | Yes | Candidate lines 18, 55, 57, 58 |
| RF-86 Custom output formats via `HelpAppendable`/`FilterHelpAppendable`; Xhtml/Apt examples | Yes | Candidate line 43 names both example renderers |
| RF-87 Custom tables via `TableDefinition` + `getTableDefinition` hook; `WeirdOptionFormat` | No | Candidate line 64 covers the hook; `example/WeirdOptionFormat.java:29` never mentioned |
| RF-88 Test packages `cli`, `.bug`, `.example`, `.help` | No | Only `.example` is referenced (line 43) |

**Covered reference facts: 56**
**Total reference facts: 88**

### Recall gaps by theme

The 32 uncovered facts cluster as follows:

1. **`Option` attribute-level semantics (RF-09, 10, 12, 13, 18, 19).** The candidate reaches `Option` through the builder and `getKey()` but never describes the attribute set, the arity constants, the `acceptsArg()`/`requiresArg()` rules, `valueSeparator` splitting, the `null`-vs-empty-array contract, or the validator's character rules.
2. **Legacy internals (RF-27, 28, 29, 46, 47, 49, 55, 58, 61, 62, 64, 77, 78, 79).** The legacy parser hierarchy is genuinely well covered here (RF-48 passes), but `Parser.processOption`, the two-pass loop's `--`/`-` handling, `Options.addOptions`, `PatternOptionBuilder`'s codes, `ParseException.wrap` semantics, and the entire deprecated `cli.HelpFormatter` remain uncovered.
3. **Help subsystem internals (RF-08, 56, 59, 71).** `FilterHelpAppendable`, `TextStyle` and `TableDefinition` are covered; the `Converter` interface's own converter constants, `DeprecatedAttributes`' content and `OptionFormatter`'s accessors are not.
4. **Fine-grained parser policy (RF-37, 39, 45).** `getLongPrefix` scanning, the throw/STOP semantics of `handleUnknownToken`, and the `handleProperties` unknown-key / `yes`-`true`-`1` rules are absent — despite the document walking the parse flow step by step.

---

## Metrics

Computed with `metrics.py` from the `evaluate-docs` skill (`python3 /Users/dariabelll/.config/opencode/skills/evaluate-docs/metrics.py 88 98 56 88`).

```
Precision: 0.8980
Recall:    0.6364
F1:        0.7449
```

| Metric | Value |
|---|---|
| Precision | 0.8980 (88/98) |
| Recall | 0.6364 (56/88) |
| F1 | 0.7449 |

### Summary

Precision is high and, notably, higher in claim density than the MiMo candidate on the parts they overlap: this document makes many more *specific, checkable* assertions (exact line citation `Options.java:158`, the `ListIterator` walk, the `scalable`-column rescaling, `Converter.DATE`'s locale fallback) and most of them verify. The 10 unsupported claims are each narrow:

- three are symbol-attribution errors — `=` attributed to `help.OptionFormatter` twice (it is `Char.EQUAL` in `Char.java:28`), and a non-existent `PatternOptionBuilder.build(Options)` method;
- two are type/contract errors — `DefaultParser.expectedOpts` called `List<Object>` (it is a raw `List`), and `CommandLine` called "immutable-ish" (it has protected mutators and exposes live collections);
- one is an invented causation — `clearValues()` attributed to mutating the shared `Options`, when the code says re-use across parses;
- one over-generalization — "the builder setters substitute defaults for `null`" (`setComparator` does not);
- one overreach — help-format customization having parse-side implications (it does not: parsers read static constants, renderers read builder instances);
- two are loose characterisations — `Option.Builder` as the "sole modern" path (three public non-deprecated constructors exist) and `TypeHandler`'s map "covering primitives" (it holds no primitive `Class` keys).

Recall is essentially level with the MiMo candidate (0.6364 vs 0.6250) but for a different reason: this document trades breadth of the model (it never enumerates `Option`'s attributes, never mentions `Options.addOptions`, and entirely omits the deprecated `cli.HelpFormatter`'s implementation) for depth of mechanics (it uniquely covers RF-14/15/16/39/43/48/50/69/70/81/82/84/86/92-94, most of which the MiMo document missed). Both documents are weakest on the same low-level `Option` semantics and on the fine-grained policy details of `Properties` defaults and `handleUnknownToken`.

---

## Reproducibility notes

- Evidence gathered only from `src/main/java/org/apache/commons/cli/**`, `src/test/java/org/apache/commons/cli/**` and `pom.xml` at commit `d95484f57dfa4b99ac9069bb3f44df680306e8e9`.
- `README.md`, `RELEASE-NOTES.txt`, `CONTRIBUTING.md`, `src/site/xdoc`, `src/changes` and POM description prose were **not** used as evidence.
- `reference-facts.md` was reused unchanged (SHA-256 verified as `51aaec37…` before and after this evaluation), so both candidates are scored against one frozen denominator.
- Neither the candidate nor the reference file was modified.
- Metrics were produced by the skill's `metrics.py`, not computed manually.
- **Caveat:** this is a self-evaluation (same model for generation and verification), which the precision figure in particular should be read in light of.