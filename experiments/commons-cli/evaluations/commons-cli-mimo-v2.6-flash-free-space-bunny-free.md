# Documentation Evaluation

## Metadata

| Field | Value |
|---|---|
| Repository | `/Users/dariabelll/Desktop/docs-llm-proj-test/commons-cli` |
| Source commit | `d95484f57dfa4b99ac9069bb3f44df680306e8e9` |
| Candidate document | `/Users/dariabelll/Desktop/generated-architecture-cli-mimo-v2.md` (read from repo-local copy `generated-architecture-cli-mimo-v2.md`) |
| Candidate SHA-256 | `0b943a5741fac862433c586161924f2ef08af7553384a4dfb665364a64764929` |
| Reference facts | `/Users/dariabelll/Desktop/docs-llm-proj-test/commons-cli/reference-facts.md` (created by the evaluator from source before the candidate was read) |
| Reference SHA-256 | `51aaec37fa3842be4a7986707bd0d90227722f13207a735a192d9ea52af16878` |
| Generating model (as declared by the requester) | MiMo-V2.6-Flash Free |
| Evaluating model | Space Bunny Free (`space-bunny-free`) |
| Evaluation date | 2026-10-09 |
| Evidence base | `src/main/java/org/apache/commons/cli/**`, `src/test/java/org/apache/commons/cli/**`, `pom.xml`, `src/conf/**`. No README/site/xdoc/AGENTS/CHANGELOG content was used as evidence. |

**Note on the candidate path.** The sandbox in this session denied `open()` on `/Users/dariabelll/Desktop/*`. At the user's instruction the file was copied byte-identically to the repository root as `generated-architecture-cli-mimo-v2.md` and read from there. The original file on the Desktop was not modified.

---

## Precision

Every independently verifiable factual claim in the candidate was extracted and checked against the source. Compound sentences were split rather than judged as a whole.

### Overview

| Claim | Verdict | Evidence |
|---|---|---|
| P-01 The project is Apache Commons CLI, coordinates `commons-cli` 1.12.0-SNAPSHOT | Supported | `pom.xml:24-32` |
| P-02 It is a Java library providing an API for defining, parsing, validating and documenting command-line interfaces | Supported | `src/main/java/org/apache/commons/cli/package-info.java:17-20`; `pom.xml:33-35` |
| P-03 It is a pure library with no server and no application entry point | Supported | No `public static void main` exists anywhere under `src/main/java/`; `pom.xml` builds a library artifact |
| P-04 Built with Maven from a single module (`pom.xml`) | Supported | Single `pom.xml` at repo root; no submodule `<modules>` list |
| P-05 Targeting Java 8 (`maven.compiler.source/target = 1.8`) | Supported | `pom.xml:89-90` |
| P-06 Produces the JPMS/OSGi name `org.apache.commons.cli` | Supported | `pom.xml:93` (`commons.module.name`), `pom.xml:99` (`commons.osgi.symbolicName`) |
| P-07 Production code lives in two packages under `src/main/java/org/apache/commons/cli/` (core API + `cli/help`) | Supported | `src/main/java/org/apache/commons/cli/` and `src/main/java/org/apache/commons/cli/help/` |
| P-08 The help-production subsystem was added in 1.10.0 | Supported | `help/AbstractHelpFormatter.java:37`, `help/HelpFormatter.java:60`, `help/package-info.java:31` |
| P-09 The library has no runtime dependencies | Supported | `pom.xml:48-84` — every `<dependency>` carries `<scope>test</scope>` |
| P-10 Every dependency (JUnit 5, Mockito, commons-io, commons-text) is test-scoped | Supported | `pom.xml:48-84` (Mockito at `pom.xml:80-84`, commons-io `pom.xml:64-69`, commons-text `pom.xml:71-78`) |

### Component: option definition model

| Claim | Verdict | Evidence |
|---|---|---|
| P-11 `Option` describes short/long name, argument arity, value separator, converter and deprecation metadata | Supported | `Option.java:390-431` |
| P-12 …and "defaults" (default values are part of the option definition model) | **Unsupported** | Evidence is insufficient: `Option` has no default-value field (`Option.java:390-431`). Option defaults are supplied at parse time through `java.util.Properties` (`DefaultParser.handleProperties`, `DefaultParser.java:492-520`), not stored on the model. |
| P-13 `Option.java` provides a `Builder`, `processValue()` and `UNLIMITED_VALUES` | Supported | `Option.java:55-353`, `Option.java:844-871`, `Option.java:365` |
| P-14 `Option` is an "immutable-ish value type" | **Unsupported** | Evidence contradicts the claim: `Option` is mutable — public setters `setDescription` (`Option.java:919`), `setRequired` (`Option.java:946`), `setType` (`Option.java:956`), `setArgs` (`Option.java:899`), `setLongOpt` (`Option.java:928`), `setOptionalArg` (`Option.java:937`), `setValueSeparator` (`Option.java:979`), `setConverter` (`Option.java:909`), `setArgName` (`Option.java:890`); its `values` list is mutated by `processValue` and cleared by `clearValues` (`Option.java:543`). |
| P-15 `Options` stores `shortOpts`, `longOpts` and `optionGroups` as maps | Supported | `Options.java:48`, `Options.java:51`, `Options.java:59` (all `LinkedHashMap`) |
| P-16 …and `requiredOpts` as a map | **Unsupported** | Evidence contradicts the claim: `requiredOpts` is a `List<Object>`, not a map (`Options.java:56`). The candidate itself states this correctly later at line 80, contradicting line 13. |
| P-17 `OptionGroup.setSelected()` throws `AlreadySelectedException` | Supported | `OptionGroup.java:134-147` |
| P-18 `OptionBuilder` is a deprecated static builder | Supported | `OptionBuilder.java:32` (`@Deprecated`), `OptionBuilder.java:40-63` (all-static state, singleton `INSTANCE`) |
| P-19 `Options.addOption()` indexes each `Option` by short key and long name | Supported | `Options.java:74-89` |
| P-20 Parsers look options up through `Options.getOption()`/`hasOption()`/`getMatchingOptions()`, clone them, and add the clones to the `CommandLine` | Supported | `Options.java:243-247`, `Options.java:308-311`, `Options.java:220-232`; `DefaultParser.java:481-483`; `Parser.java:254-262` |
| P-21 The help subsystem reads the same `Options`/`Option` objects (descriptions, `since`, required flags) to render usage tables | Supported | `AbstractHelpFormatter.java:327-344`, `help/HelpFormatter.java:180-199`, `AbstractHelpFormatter.java:489-495` |

### Component: parsing layer

| Claim | Verdict | Evidence |
|---|---|---|
| P-22 Purpose: turns a `String[]` of raw arguments plus an `Options` descriptor into a populated `CommandLine`, enforcing required options, groups and argument-count rules | Supported | `CommandLineParser.java:24-34`, `DefaultParser.java:739-762`, `OptionGroup.java:134-147` |
| P-23 `CommandLineParser.java` defines the `parse(Options, String[])` contract | Supported | `CommandLineParser.java:34` (and the `stopAtNonOption` overload at line 48) |
| P-24 `DefaultParser` is the current single-pass parser (since 1.3) with a nested `Builder` and a `NonOptionAction` enum | Supported | `DefaultParser.java:33-35`, `DefaultParser.java:47`, `DefaultParser.java:159-177`; single-pass: tokens are handled in a loop inside `parse` (`DefaultParser.java:751-755`) with no `flatten` phase |
| P-25 `Parser.java` is a deprecated abstract two-pass "flatten" parser with `BasicParser`, `PosixParser`, `GnuParser` subclasses | Supported | `Parser.java:32-35`, `Parser.java:74`, `BasicParser.java:26`, `PosixParser.java`, `GnuParser.java:30` |
| P-26 `ParseException` with subclasses `MissingOptionException`, `MissingArgumentException`, `UnrecognizedOptionException`, `AmbiguousOptionException`, `AlreadySelectedException` | Supported | `ParseException.java:23`, `MissingOptionException.java:25`, `MissingArgumentException.java:23`, `UnrecognizedOptionException.java:23`, `AmbiguousOptionException.java:28`, `AlreadySelectedException.java:23` |
| P-27 `DefaultParser` reads `Options`, clones matched `Option`s into the `CommandLine` it builds (`handleOption()`) | Supported | `DefaultParser.java:478-485`, `DefaultParser.java:741`, `DefaultParser.java:750` |
| P-28 `DefaultParser` invokes `Option.processValue()` for argument tokens | Supported | `DefaultParser.java:403`, `DefaultParser.java:449`, `DefaultParser.java:555`, `DefaultParser.java:560`, `DefaultParser.java:576`, `DefaultParser.java:584-585`, `DefaultParser.java:608` |
| P-29 `DefaultParser` tracks group selection via `Options.getOptionGroup()` | Supported | `DefaultParser.java:851-852` |
| P-30 `DefaultParser` resolves the option-prefix constants from `help/OptionFormatter` (`"-"`, `"--"`) | Supported | `DefaultParser.java:28` (import), `DefaultParser.java:605`, `DefaultParser.java:611`, `OptionFormatter.java:279`, `OptionFormatter.java:284` |
| P-31 It reuses `Util.stripLeadingHyphens()` / `stripLeadingAndTrailingQuotes()` | Supported | `DefaultParser.java:346`, `DefaultParser.java:534`, `DefaultParser.java:823`, `DefaultParser.java:836`, `Util.java:58-86` |
| P-32 The deprecated `Parser` hierarchy implements the same contract but pre-flattens tokens via the abstract `flatten()` | Supported | `Parser.java:35`, `Parser.java:74`, `Parser.java:162-203` |

### Component: result model (`CommandLine`)

| Claim | Verdict | Evidence |
|---|---|---|
| P-33 `CommandLine` holds parsed options and leftover positional arguments and exposes `hasOption`, `getOptionValue(s)`, `getParsedOptionValue(s)`, `getOptionProperties`, `getArgList` | Supported | `CommandLine.java:150-153`, `CommandLine.java:963-1013`, `CommandLine.java:221-232`, `CommandLine.java:307-335`, `CommandLine.java:490-539`, `CommandLine.java:551-926` |
| P-34 `CommandLine.java` has a nested `Builder` and `resolveOption()` | Supported | `CommandLine.java:48-135`, `CommandLine.java:1035-1043` |
| P-35 …and "~50 `getOptionValue`/`getParsedOptionValue` overloads" | **Unsupported** | Evidence contradicts the approximation: the four families declare 40 public overloads in total — 12 `getOptionValue` (`CommandLine.java:352-481`), 4 `getOptionValues` (`:490-539`), 12 `getParsedOptionValue` (`:551-730`), 12 `getParsedOptionValues` (`:742-926`). 40 is not ~50. |
| P-36 `CommandLine` is built by both parser families through `CommandLine.builder()` | Supported | `DefaultParser.java:750`, `Parser.java:160` |
| P-37 It resolves names back to `Option` instances with `Util.stripLeadingHyphens` | Supported | `CommandLine.java:1035-1043`, `Util.java:75-86` |
| P-38 It converts string values with `Option.getConverter()`, falling back to `TypeHandler.getDefault()` | Supported | `CommandLine.java:620`, `CommandLine.java:814`, `Option.java:610-612` |
| P-39 It invokes the injected `deprecatedHandler` (`Consumer<Option>`, default prints to `System.out`) when a deprecated option is queried | Supported | `CommandLine.java:53`, `CommandLine.java:933-937`, `CommandLine.java:976-979`, `CommandLine.java:508-510` |

### Component: type conversion

| Claim | Verdict | Evidence |
|---|---|---|
| P-40 Converts raw option value strings into typed objects (`File`, `URL`, `Date`, `Number`, `Class`, …) | Supported | `TypeHandler.java:220-251`, `Converter.java:41-108` |
| P-41 `Converter.java` is a functional interface with a `DEFAULT` identity converter | Supported | `Converter.java:34-41` |
| P-42 `TypeHandler.java` has `createDefaultMap()` and a singleton `getDefault()` | Supported | `TypeHandler.java:80-82`, `TypeHandler.java:45`, `TypeHandler.java:203-205` |
| P-43 `PatternOptionBuilder.java` maps legacy pattern codes to classes / converter lookup | Supported | `PatternOptionBuilder.java:132-156`, `PatternOptionBuilder.java:210-214` |
| P-44 The converter is selected per option via `Option.Builder.converter(...)` or `Option.type` | Supported | `Option.java:149-154`, `Option.java:314-317`, `Option.java:610-612` |
| P-45 It is consumed by `CommandLine.getParsedOptionValue*()` | Supported | `CommandLine.java:620`, `CommandLine.java:814` |
| P-46 …and by `OptionBuilder.withType()` | Supported | `OptionBuilder.java:271` |
| P-47 Several `TypeHandler` static factory methods are deprecated in favour of converters | Supported | `TypeHandler.java:106`, `:120`, `:133`, `:175`, `:215` |

### Component: help production subsystem

| Claim | Verdict | Evidence |
|---|---|---|
| P-48 Pluggable pipeline: a formatter decides *what* to show, an `OptionFormatter` decides how each option is spelled, a `TableDefinition` describes the layout, a `HelpAppendable` decides the output format | Supported | `AbstractHelpFormatter.java:33-38`, `AbstractHelpFormatter.java:285`, `TableDefinition.java:36`, `HelpAppendable.java:24-120`, `OptionFormatter.java:28-31` |
| P-49 `AbstractHelpFormatter` provides `printHelp()`, `toSyntaxOptions()`, an abstract `getTableDefinition()` and a self-typed `Builder` | Supported | `AbstractHelpFormatter.java:296-344`, `:431-508`, `:285`, `:51-165` |
| P-50 `help/HelpFormatter.java` is the default implementation with a 2- or 3-column table and an optional "Since" column | Supported | `HelpFormatter.java:163-208`; with `showSince=true` (default, `:75`) three columns are emitted, with `false` two (`HelpFormatter.java:201-207`) |
| P-51 `OptionFormatter.java`, `TableDefinition.java`, `TextStyle.java` are key source locations of the subsystem | Supported | Files exist with those responsibilities (`OptionFormatter.java:32`, `TableDefinition.java:36`, `TextStyle.java:28`) |
| P-52 `HelpAppendable.java`, `TextHelpAppendable.java` (word-wrapping text renderer) and `FilterHelpAppendable.java` (decorator base) are key source locations | Supported | `HelpAppendable.java:37`, `TextHelpAppendable.java:35`, `:362-393`, `FilterHelpAppendable.java:38-72` |
| P-53 `HelpFormatter.printHelp()` writes the syntax line via `toSyntaxOptions(Options)` (honouring `OptionGroup`s), then `helpAppendable.appendTable(getTableDefinition(options.getOptions()))` | Supported | `AbstractHelpFormatter.java:332-340`, `:442-472`, `:506-508`, `:362-374` |
| P-54 The help subsystem depends on the core model (`Options`, `Option`, `OptionGroup`) | Supported | `AbstractHelpFormatter.java:29-31`, `help/HelpFormatter.java:23`, `help/OptionFormatter.java:24-25` |
| P-55 …but "nothing in the core model depends on it" | **Unsupported** | Evidence contradicts the claim: six core-package classes import `org.apache.commons.cli.help` — `Util.java:20`, `OptionGroup.java:26`, `DefaultParser.java:28`, `Parser.java:27`, `PosixParser.java:25`, `GnuParser.java:23` (plus the legacy `HelpFormatter.java:37-38`). The dependency is bidirectional; `Util` and `OptionGroup` (core model classes) use `OptionFormatter.DEFAULT_OPT_PREFIX`/`DEFAULT_LONG_OPT_PREFIX`. The candidate contradicts itself: line 25 states that `DefaultParser` resolves its prefix constants from `help/OptionFormatter`. |
| P-56 Test sources show custom renderers (`XhtmlHelpAppendable.java`, `AptHelpAppendable.java`) | Supported | `src/test/java/org/apache/commons/cli/example/XhtmlHelpAppendable.java:32`, `src/test/java/org/apache/commons/cli/example/AptHelpAppendable.java:34` (both `extends FilterHelpAppendable`) |
| P-57 The legacy `cli/HelpFormatter.java` is deprecated and renders independently through a `PrintWriter` without using the help subsystem | Supported | `HelpFormatter.java:73-74` (`@Deprecated`), `:326` (`PrintWriter printWriter`); it never references `AbstractHelpFormatter` as a supertype, `HelpAppendable`, `TextHelpAppendable` or `TableDefinition` — only two constants (`HelpFormatter.java:37-38`, `:206-209`, `:404`) |

### Data / control flow

| Claim | Verdict | Evidence |
|---|---|---|
| P-58 Step 1 — the application builds an `Options` descriptor; `addOption` indexes each `Option` into `shortOpts`/`longOpts`; `addOptionGroup` registers groups and clears member `required` flags | Supported | `Options.java:74-89`, `Options.java:150-165` |
| P-59 Step 2 — `DefaultParser.parse(options, properties, nonOptionAction, arguments...)` resets parser state, clears group selections, copies `options.getRequiredOptions()` into `expectedOpts`, and creates a `CommandLine` via `CommandLine.builder()` | Supported | `DefaultParser.java:739-762` (`:743-745`, `:747-749`, `:750`) |
| P-60 Step 3a — `--` sets `skipParsing`, and all remaining tokens become arguments | Supported | `DefaultParser.java:605-606`, `:603-604` |
| P-61 Step 3b — if the current option accepts an argument and the token is not an option (or is a negative number), it is consumed via `currentOption.processValue(...)` with quote stripping applied | Supported | `DefaultParser.java:607-608`, `:648-650`, `:690-697`, `:704-706`, `:834-839` |
| P-62 Step 3c — `--long` / `-long` forms route to `handleLongOption*()` | Supported | `DefaultParser.java:609-610` → `handleLongOption` (`:418-424`); `-long` goes through `handleShortAndLongOption` (`:611-612`) which delegates to `handleLongOptionWithoutEqual` (`:547-549`) |
| P-63 Step 3c — partial matching may yield `AmbiguousOptionException` | Supported | `DefaultParser.java:442-443`, `:470-471` |
| P-64 Step 3c — `--name=value` splits at `=` | Supported | `DefaultParser.java:435-437`, `indexOfEqual` at `:189-191` |
| P-65 Step 3d — `-x` forms route to `handleShortAndLongOption()` (single short, concatenated `-abc`, Java-style `-Dkey=value`, long-prefix `-Xmx512m`, or `-S=V`) | Supported | `DefaultParser.java:533-592`; single short `:536-542`, concatenated `:564`/`handleConcatenatedOptions` `:393-407`, Java property `:557-561` and `:581-586`, long prefix `:551-556`, `-S=V` `:571-580` |
| P-66 Step 3e — anything else hits `handleUnknownToken()`, which applies the `NonOptionAction` (IGNORE/SKIP/STOP/THROW) | Supported | `DefaultParser.java:613-615`, `:630-641`, `:159-177` |
| P-67 Step 4 — `handleOption()` clones the matched `Option`, records it on the `CommandLine`, updates group selection and removes satisfied required entries from `expectedOpts` | Supported | `DefaultParser.java:478-485` → `updateRequiredOptions` `:846-858` |
| P-68 Step 5 — `checkRequiredArgs()` → `handleProperties(properties)` (default values for absent options) → `checkRequiredOptions()` throws `MissingOptionException` if unmet | Supported | `DefaultParser.java:756-760`, `:492-520`, `:333-338`, `MissingOptionException.java:25` |
| P-69 Step 6 — the application queries the returned `CommandLine` and may call `HelpFormatter.printHelp(...)` | Supported | `CommandLine.java:963-1013`, `:551-730`, `AbstractHelpFormatter.java:327-344` |

### Diagram (mermaid)

| Claim | Verdict | Evidence |
|---|---|---|
| P-70 `Options`/`Option`/`OptionGroup` definition → `DefaultParser` or deprecated `Parser`/`Posix`/`Gnu`/`Basic` | Supported | `CommandLineParser.java:34` implemented by `DefaultParser.java:35` and `Parser.java:35` (+ the three subclasses) |
| P-71 Parser → `CommandLine` ("cloned Options + args") | Supported | `DefaultParser.java:481-483`, `:313`; `Parser.java:254-262` |
| P-72 `CommandLine` → `Converter`/`TypeHandler` → typed values | Supported | `CommandLine.java:620`, `Option.java:610-612`, `TypeHandler.java:290-292` |
| P-73 Definition model → `help.HelpFormatter` | Supported | `AbstractHelpFormatter.java:327-344`, `help/HelpFormatter.java:163-208` |
| P-74 `help.HelpFormatter` → `OptionFormatter` + `TableDefinition` | Supported | `help/HelpFormatter.java:183`, `:207`, `AbstractHelpFormatter.java:248-250` |
| P-75 `OptionFormatter` + `TableDefinition` → `HelpAppendable` | Supported | `AbstractHelpFormatter.java:340`, `:372-374`, `TextHelpAppendable.java:243-254` |
| P-76 Parser → throws → `ParseException` hierarchy | Supported | `DefaultParser.java:632`, `:443`, `:324`, `:336`, `OptionGroup.java:144`; hierarchy per `ParseException.java:23` and subclasses |

### Key decisions & gotchas

| Claim | Verdict | Evidence |
|---|---|---|
| P-77 `DefaultParser` mutates instance fields (`cmd`, `currentOption`, `skipParsing`, `expectedOpts`) during `parse()` | Supported | `DefaultParser.java:194`, `:219`, `:222`, `:227`; assigned at `:743-750`, `:484`, `:617`, `:639`, `:663` |
| P-78 Both parser families clone each matched `Option` before adding it to `CommandLine` | Supported | `DefaultParser.java:481`, `Parser.java:254` |
| P-79 …while clearing prior **option values** at the start of every parse (comment referencing CLI-71 in `Parser.java:152`) | **Unsupported** | Evidence contradicts the claim: only the deprecated `Parser` clears option values — `Parser.java:153` (`options.helpOptions().forEach(Option::clearValues)`). `DefaultParser.parse` performs no `clearValues` call at all (`:739-762`); `clearValues` has exactly one caller in the whole main source set (`Parser.java:153`). `Parser.java:152` is indeed the CLI-71 comment, but attributing the behaviour to both families is wrong. |
| P-80 …while clearing prior **group selections** at the start of every parse | Supported | `Parser.java:155-157`, `DefaultParser.java:747-749` |
| P-81 One parser instance must not be used concurrently | Supported | Parser instances keep mutable parse state on `this` (`DefaultParser.java:194-227`, `Parser.java:38-44`, `PosixParser` `tokens`/`currentOption`), with no synchronisation anywhere in the main source set |
| P-82 `Options.requiredOpts` is a `List<Object>` holding both `String` option keys and `OptionGroup` objects | Supported | `Options.java:56`, populated at `:85` (key) and `:152` (group) |
| P-83 `DefaultParser.expectedOpts` is a `List<Object>` | **Unsupported** | Evidence contradicts the claim: `expectedOpts` is declared as a **raw** `List`, not `List<Object>` — `DefaultParser.java:227` (`protected List expectedOpts;`). |
| P-84 Both lists are flagged by the authors with `// TODO this seems wrong` | Supported | `Options.java:55`, `DefaultParser.java:226` (the candidate cites `Options.java:54` / `DefaultParser.java:225`, which are the adjacent explanatory comment lines — off by one, but the flag is present as described) |
| P-85 Tri-state quote stripping: `true` always strips, `false` never, `null` (default, historic) strips only for space-separated values | Supported | `DefaultParser.java:61`, `:148-151`, `:821-839` |
| P-86 `NonOptionAction` (since 1.10.0) generalises the older boolean `stopAtNonOption`, whose deprecated field is retained in `DefaultParser` purely for binary compatibility | Supported | `DefaultParser.java:199-206` ("This field is unused, and left for binary compatibility reasons"), `:159-177`, `:812` |
| P-87 Long-option partial matching is on by default; `Options.getMatchingOptions()` does prefix matching; multiple candidates without an exact match raise `AmbiguousOptionException` unless built with `setAllowPartialMatching(false)` | Supported | `DefaultParser.java:50`, `:263` (default `true`), `:116-119`, `:365-374`; `Options.java:220-232`; `DefaultParser.java:442-443`, `:470-471` |
| P-88 `Parser` + `BasicParser`/`PosixParser`/`GnuParser` (two-pass flatten) are deprecated | Supported | `Parser.java:34`, `BasicParser.java:26`, `PosixParser.java`, `GnuParser.java:30` |
| P-89 The static mutable `OptionBuilder` is deprecated and explicitly documented as NOT thread safe | Supported | `OptionBuilder.java:32`, `:29` (CLI-209 reference), `:40-63` |
| P-90 The root `HelpFormatter` is deprecated | Supported | `HelpFormatter.java:73` |
| P-91 `build()` methods on the builders are deprecated in favour of `Supplier.get()` | Supported | `Option.Builder.build()` `Option.java:134-137`; `CommandLine.Builder.build()` `CommandLine.java:108-111`; `DefaultParser.Builder.build()` `DefaultParser.java:79-82`; `OptionBuilder.Builder` constructors `OptionBuilder.java:65-67`, `DeprecatedAttributes.Builder` `DeprecatedAttributes.java:63-67` |
| P-92 The default goal runs `japicmp:cmp` against `commons.bc.version = 1.11.0` to enforce API compatibility | Supported | `pom.xml:98` (`<commons.bc.version>1.11.0</commons.bc.version>`), `pom.xml:115` (`<defaultGoal>` includes `japicmp:cmp`), `pom.xml:165-168` (japicmp plugin in `<build><plugins>`). The exact `oldVersion` binding is inherited from `commons-parent:105`, which is not vendored in this repository — the property, the goal and the plugin declaration are all confirmed in-repo. |
| P-93 `CommandLine.hasOption(Option)` invokes the transient `Consumer<Option> deprecatedHandler` (default: print `Option.toDeprecatedString()` to `System.out`) whenever a deprecated option is checked; the field is `transient`, with an in-code warning to use a serialization proxy | Supported | `CommandLine.java:162` (field + warning), `:53` (default handler), `:974-979` (`hasOption(Option)`), `Option.java:983-998` |
| P-94 `pom.xml` sets JaCoCo halt-on-failure thresholds of 98% instruction/line and 95% branch | Supported | `pom.xml:106` (`haltOnFailure`), `:108` (instruction 0.98), `:110` (branch 0.95), `:111` (line 0.98) |
| P-95 `pom.xml` wires Checkstyle, SpotBugs, PMD, RAT and Javadoc into the default Maven goal | Supported | `pom.xml:115` (`clean verify apache-rat:check japicmp:cmp checkstyle:check spotbugs:check pmd:check javadoc:javadoc`); plugin declarations at `pom.xml:119-193` |

**Supported claims: 78**
**Total claims: 85**

---

## Recall

Reference set: 88 architectural facts (`reference-facts.md`), frozen from source at commit `d95484f57dfa4b99ac9069bb3f44df680306e8e9` before the candidate was read.

| Reference fact | Covered | Evidence |
|---|---|---|
| RF-01 Single-module Maven project, one root `pom.xml` | Yes | Candidate line 5 |
| RF-02 Maven coordinates `commons-cli` / `1.12.0-SNAPSHOT`, parent `commons-parent:105` | Yes | Candidate line 5 (coordinates); parent POM confirmed at `pom.xml:27-31` |
| RF-03 Java 8 source/target | Yes | Candidate line 5; `pom.xml:89-90` |
| RF-04 No compile/runtime dependencies; all test-scoped | Yes | Candidate line 5; `pom.xml:48-84` |
| RF-05 36 main / 51 test Java files | No | Not mentioned anywhere in the candidate |
| RF-06 Two production packages `cli` and `cli.help` | Yes | Candidate line 5; directory listing |
| RF-07 `help` package names four user-facing types (`HelpFormatter`, `HelpAppendable`, `OptionFormatter`, `TableDefinition`) | Yes | Candidate lines 42-47 names all four; `help/package-info.java:19-30` |
| RF-08 `cli.Util` and `cli.Char` are package-private internal helpers; a separate package-private `help.Util` exists | No | Candidate mentions `Util` (lines 25, 31) but never `Char` and never `help/Util.java`; `Char.java:23`, `help/Util.java:25` uncovered |
| RF-09 `Option` is a `Cloneable, Serializable` value object with the full attribute set | Yes | Candidate line 10 enumerates the attributes; `Option.java:41`, `:390-431` |
| RF-10 Argument-count constants `UNINITIALIZED = -1` and `UNLIMITED_VALUES = -2` with their semantics | No | Candidate names `UNLIMITED_VALUES` (line 12) as a bare symbol with no semantics and never mentions `UNINITIALIZED`; `Option.java:362-365` uncovered |
| RF-11 `Option` is created via nested `Option.Builder`; the name is validated by `OptionValidator.validate` | Yes | Candidate lines 12 and 15; `Option.java:259-262`, `OptionBuilder.java`/`OptionValidator.java` cited as key locations |
| RF-12 `hasArg()` / `hasArgs()` / `acceptsArg()` / `requiresArg()` semantics | No | Never described; `Option.java:507-509`, `:755-775`, `:878-883` uncovered |
| RF-13 `Option.processValue` splits on `valueSeparator` and stops after `argCount-1` values | No | Candidate mentions `processValue()` only as a call target (lines 18, 58); the splitting rule (`Option.java:844-871`) is not described |
| RF-14 `Option.clone()` duplicates the `values` list so each occurrence carries its own values | No | Candidate says only "clone them"/"clones the matched Option" (lines 16, 25, 62); `Option.java:556-565` uncovered |
| RF-15 `Option.clearValues()` empties stored values between parses (CLI-71) | No | Candidate references CLI-71 only as a comment citation and misattributes the call to both parsers (line 79); `Option.java:543-545` uncovered |
| RF-16 `Option.getKey()` = short name else long name; identifier for required tracking and group membership | No | Never described; `Option.java:648-651` uncovered |
| RF-17 `Option.getConverter()` falls back to `TypeHandler.getDefault().getConverter(type)` | Yes | Candidate lines 31, 64, 28; `Option.java:610-612` |
| RF-18 `getValues()` returns `null` (not an empty array) when empty | No | Never mentioned; `Option.java:728-730` uncovered |
| RF-19 `OptionValidator` rules — `?`/`@` as first char, `-` allowed afterwards | No | Candidate lists the file only (line 15); `OptionValidator.java:28-31`, `:51-53`, `:122-145` uncovered |
| RF-20 `OptionGroup` internals (ordered option map, `selected`, `required`) | No | Only the component name and one method appear (line 14); `OptionGroup.java:39-45` uncovered |
| RF-21 `OptionGroup.setSelected` throws `AlreadySelectedException` on a different member; `null` resets; `isSelected()` | Yes | Candidate line 14; `OptionGroup.java:134-147` |
| RF-22 `Options` is the main entry point / registry with four collections | Yes | Candidate lines 13, 16, 54; `Options.java:31-59` |
| RF-23 `Options.addOption` registers in `longOpts`/`shortOpts` and appends to `requiredOpts` when required | Yes | Candidate lines 16, 54; `Options.java:74-89` |
| RF-24 `Options.addOptionGroup` forces members optional, removes them from `requiredOpts`, maps key→group | Yes | Candidate line 54 ("clears member `required` flags"); `Options.java:150-165` |
| RF-25 Lookups normalise names via `Util.stripLeadingHyphens`, short map first, long map as fallback | Yes | Candidate lines 25, 31; `Options.java:243-247`, `:298-323` |
| RF-26 `Options.getMatchingOptions` implements long-option prefix/partial matching | Yes | Candidate lines 16, 83; `Options.java:220-232` |
| RF-27 `getRequiredOptions` unmodifiable / `getOptionGroups` de-duplicates via `HashSet` / `getOptions` unmodifiable | No | Never described; `Options.java:264-289`, `:330-332` uncovered |
| RF-28 `Options.addOptions` throws `IllegalArgumentException` on duplicate keys | No | Never mentioned; `Options.java:175-184` uncovered |
| RF-29 `Options` offers a fluent API returning `this` | No | Never mentioned; `Options.java:74-211` uncovered |
| RF-30 `CommandLineParser` SPI: `parse(Options, String[])` and the `stopAtNonOption` overload | Yes | Candidate lines 21, 23; `CommandLineParser.java:34`, `:48` |
| RF-31 `DefaultParser` is single-pass; `Parser` is a deprecated two-pass `flatten` design | Yes | Candidate line 22 ("current single-pass parser") and line 23 ("deprecated abstract two-pass 'flatten' parser") |
| RF-32 `DefaultParser` configurable state: `allowPartialMatching` (default true), tri-state quote stripping, `deprecatedHandler`, via `builder()` | Yes | Candidate lines 22, 81, 82, 83; `DefaultParser.java:47-152`, `:230-243` |
| RF-33 `NonOptionAction` enum (IGNORE/SKIP/STOP/THROW); boolean overloads delegate to STOP/THROW | Yes | Candidate lines 22, 61, 82; `DefaultParser.java:159-177`, `:812` |
| RF-34 Canonical `parse(Options, Properties, NonOptionAction, String...)` entry point and its sequence | Yes | Candidate lines 55, 63; `DefaultParser.java:739-762` |
| RF-35 `handleToken` dispatch order (skipParsing → `--` → value → long → short → unknown) | Yes | Candidate lines 56-61 enumerate the same branches in the same order; `DefaultParser.java:600-620` |
| RF-36 `handleShortAndLongOption` handles `-S`, `-S=V`, `-L`, `-L=V`, `-LV`, `-S1S2`, `-Dkey[=value]`, `-Xmx512m` | Yes | Candidate line 60 lists the forms; `DefaultParser.java:533-592` |
| RF-37 `getLongPrefix` scans prefixes longest-to-shortest for JVM-style attached values | No | Candidate line 60 names `-Xmx512m` but not the prefix-scanning mechanism; `DefaultParser.java:345-357` uncovered |
| RF-38 Ambiguous partial matches raise `AmbiguousOptionException` | Yes | Candidate lines 59, 83; `DefaultParser.java:442-443`, `:470-471` |
| RF-39 `handleUnknownToken` throws only when the action is THROW; STOP sets `skipParsing` | Yes | Candidate lines 57, 61; `DefaultParser.java:630-641` |
| RF-40 `isArgument` = not an option or a negative number (`Double.parseDouble`) | Yes | Candidate line 58; `DefaultParser.java:648-650`, `:690-697` |
| RF-41 Tri-state quote stripping with separate DefaultOn/DefaultOff call sites | Yes | Candidate lines 58, 81; `DefaultParser.java:821-839` |
| RF-42 Every parsed occurrence is cloned and the clone becomes `currentOption` when it takes an argument | Yes | Candidate lines 25, 62; `DefaultParser.java:478-485` |
| RF-43 `checkRequiredArgs` throws `MissingArgumentException`, except for a single-value Java-property option | No | Candidate line 63 names the method but not the exception or the `-Dflag` exemption; `DefaultParser.java:319-326` uncovered |
| RF-44 `updateRequiredOptions` removes the key/group from `expectedOpts` and marks the group selection | Yes | Candidate line 62; `DefaultParser.java:846-858` |
| RF-45 `handleProperties` semantics — unknown key throws, skips set options/selected groups, `yes`/`true`/`1` for flags | No | Candidate line 63 says only "default values for absent options"; `DefaultParser.java:492-520` uncovered |
| RF-46 Deprecated `Parser` two-pass loop: `--`/`-` handling, `stopAtNonOption` eats the rest, single `--` | No | Only "two-pass" is stated (line 23); the loop behaviours of `Parser.java:162-203` are not described |
| RF-47 `Parser.parse` resets state (clears option values, clears group selections, snapshots required options) | Yes | Candidate line 79 ("clearing prior values/group selections at the start of every parse (comment referencing CLI-71 in `Parser.java:152`)") — correct for the `Parser` family; `Parser.java:152-160`, `:311-314` |
| RF-48 `BasicParser`/`GnuParser`/`PosixParser` `flatten` behaviours (echo, `-Dkey=value` splitting, bursting, ambiguity) | No | Candidate line 23 names the three subclasses but describes none of their `flatten` semantics |
| RF-49 `Parser.processOption` — throws `UnrecognizedOptionException`, clones, `processArgs`, `MissingArgumentException` | No | Never described; `Parser.java:247-263`, `:217-237` uncovered |
| RF-50 `CommandLine` internals: args `LinkedList`, options `ArrayList` of clones, transient handler, `Serializable`, `builder()` | Yes | Candidate lines 27-31, 69; `CommandLine.java:41`, `:150-178` |
| RF-51 `resolveOption` strips hyphens and matches `getOpt()`/`getLongOpt()` | Yes | Candidate line 31; `CommandLine.java:1035-1043` |
| RF-52 Value-lookup API surface (`hasOption` variants, `getOptionValue(s)`, `getOptionProperties`, `getOptionCount`, `iterator`, `getArgs`, `getArgList`) | Yes | Candidate line 28 lists `hasOption`, `getOptionValue(s)`, `getParsedOptionValue(s)`, `getOptionProperties`, `getArgList` — `getOptionCount`/`iterator`/`getArgs` omitted but the model's query responsibility is established; `CommandLine.java:221-265`, `:963-1013` |
| RF-53 Typed access via `Option.getConverter()` with `ParseException.wrap`; array variant uses `Array.newInstance` | Yes | Candidate lines 28, 31, 64; `CommandLine.java:610-624`, `:801-820` |
| RF-54 Deprecation warnings emitted lazily on query through `deprecatedHandler`; default prints `toDeprecatedString()` | Yes | Candidate lines 31, 85; `CommandLine.java:53`, `:933-937`, `:976-979` |
| RF-55 `getOptionProperties` pairs values (odd trailing value → `"true"`); `getOptionValue(OptionGroup)` delegates to the selected option | No | Candidate names `getOptionProperties` (line 28) without its pairing rule; `CommandLine.java:1023-1027`, `:422-424` uncovered |
| RF-56 `Converter<T,E>` functional interface with predefined converters (DEFAULT/CLASS/FILE/PATH/NUMBER/OBJECT/URL/DATE) | Yes | Candidate lines 34, 36 state the responsibility and the `DEFAULT` identity converter; `Converter.java:34-108` |
| RF-57 `TypeHandler` converter map, singleton `getDefault()`, default registrations, `Converter.DEFAULT` fallback | Yes | Candidate lines 31, 37; `TypeHandler.java:45`, `:80-82`, `:203-205`, `:220-251`, `:290-292` |
| RF-58 `TypeHandler` static helpers mostly deprecated; `ParseException.wrap`; `createFiles`/`createDate` unimplemented | Yes | Candidate line 37; `TypeHandler.java:57-218`, `:106-111` |
| RF-59 `DeprecatedAttributes` immutable value object (`description`, `since`, `forRemoval`) with a `Builder` | No | Candidate line 15 lists the file as a key location only, with no responsibility; `DeprecatedAttributes.java:34`, `:128-134` uncovered |
| RF-60 `OptionBuilder` is static-state and not thread safe (CLI-209) | Yes | Candidate line 84; `OptionBuilder.java:29`, `:40-63` |
| RF-61 `PatternOptionBuilder.parsePattern` value codes and `!` for required | No | Candidate line 38 says only "legacy pattern codes → classes/converter lookup"; the codes, `!`, and the deliberately unsupported `File[]` converter (`PatternOptionBuilder.java:132-156`, `:210-214`) are not covered |
| RF-62 `ParseException` is a checked exception extending `Exception`, plus `ParseException.wrap` | No | Candidate line 24 names the class but not that it is checked, nor `wrap` (`ParseException.java:23`, `:44-52`) |
| RF-63 `ParseException` subtype taxonomy | Yes | Candidate line 24 enumerates the hierarchy; `ParseException.java:23` and the five subclasses |
| RF-64 `AmbiguousOptionException extends UnrecognizedOptionException` and carries matching names | No | Candidate line 24 lists it flatly as a `ParseException` subclass; the intermediate `UnrecognizedOptionException` parent (`AmbiguousOptionException.java:28`) is not established |
| RF-65 `HelpAppendable` is the output SPI: `Appendable` plus semantic `appendHeader`/`appendList`/`appendParagraph`/`appendTable`/`appendTitle` | Yes | Candidate lines 42, 43, 48, 53 give the role and show `appendTable`; `HelpAppendable.java:24-120` |
| RF-66 `FilterHelpAppendable` delegates the `Appendable` primitives to an underlying `Appendable` and is the base for output filters | No | Candidate line 47 labels it only "decorator base" with no mechanism; `FilterHelpAppendable.java:38-72` uncovered |
| RF-67 `TextHelpAppendable` renders wrapped plain text with the documented width/pad/indent constants and resizes table columns | Yes | Candidate line 47 ("word-wrapping text renderer") and line 45 (table layout); `TextHelpAppendable.java:35-49`, `:152-265`, `:362-393` |
| RF-68 `TableDefinition` is an immutable table description (`caption`, `TextStyle`s, `headers`, `rows`) with `from(...)` | Yes | Candidate line 42 ("describes the layout") and line 46; `TableDefinition.java:36-101` |
| RF-69 `TextStyle` is the immutable column/paragraph style with alignment, indent, leftPad, min/max width, `scalable`, `pad` | No | Candidate line 46 lists the file only, with no responsibility; `TextStyle.java:28`, `:236-392` uncovered |
| RF-70 `OptionFormatter` defaults (`-`, `--`, `", "`, `" "`, `"arg"`, `[`/`]`, `<`/`>`) and deprecated-format functions | No | Candidate line 42 states the role but no defaults; `OptionFormatter.java:228-294` uncovered |
| RF-71 `OptionFormatter` accessors (`getBothOpt`, `getArgName`, `getDescription`, `getSince`, `toSyntaxOption`, `toOptional`) | No | Never listed; `OptionFormatter.java:384-480` uncovered |
| RF-72 `AbstractHelpFormatter` binds a `HelpAppendable` + `OptionFormatter.Builder` + comparator + group separator + syntax prefix; self-typed `Builder` with those defaults | Yes | Candidate line 44 names the framework, the four collaborators and the self-typed `Builder`; `AbstractHelpFormatter.java:33-38`, `:51-213` |
| RF-73 `printHelp` composes usage paragraph, header, option table and footer; empty syntax raises `IllegalArgumentException` | Yes | Candidate line 53 (syntax line then table) plus line 48; `AbstractHelpFormatter.java:327-344` |
| RF-74 `toSyntaxOptions` emits each group once, joins members with the separator, wraps non-required in optional delimiters | Yes | Candidate line 53 ("`toSyntaxOptions(Options)`, which honors `OptionGroup`s"); `AbstractHelpFormatter.java:442-508` |
| RF-75 `help.HelpFormatter` renders an `Options`/`Since`/`Description` table, `showSince` default true, width 74 / left pad 1 / column spacing 5 | Yes | Candidate line 45; `HelpFormatter.java:72-132`, `:163-208` |
| RF-76 Plug points `setHelpAppendable` / `setOptionFormatBuilder` make the subsystem format-agnostic | Yes | Candidate line 42 (pluggable pipeline) and line 48 (custom renderers); `AbstractHelpFormatter.java:132-151` |
| RF-77 Legacy `HelpFormatter` is `@Deprecated`, independent, `PrintWriter`-based, does not extend/use the help subsystem | Yes | Candidate line 48; `HelpFormatter.java:37-38`, `:73-74`, `:326` |
| RF-78 Legacy formatter's mutable rendering state and method set (`printUsage`, `renderOptions`, `findWrapPos`, …) | No | Candidate line 48 says only that it "renders independently through a `PrintWriter`"; `HelpFormatter.java:545-995` uncovered |
| RF-79 One-way compatibility aliasing (`cli.HelpFormatter.DEFAULT_OPT_PREFIX` → `help.OptionFormatter` constants) | No | Not described; `HelpFormatter.java:206-209` uncovered |
| RF-80 Definition flow (build `Option`s → register in `Options` → hand to a parser) | Yes | Candidate lines 16, 54; `Option.java:373-499`, `Options.java:74-165` |
| RF-81 Modern parse flow end to end | Yes | Candidate lines 52-64; `DefaultParser.java:739-762` |
| RF-82 Legacy parse flow (`flatten` → shared loop → properties → required check) | Yes | Candidate lines 23, 25, 79; `Parser.java:150-207` |
| RF-83 Help flow (formatter → syntax line + table → `HelpAppendable` → wrapped/rescaled output) | Yes | Candidate lines 48, 64; `AbstractHelpFormatter.java:327-344`, `TextHelpAppendable.java:243-254` |
| RF-84 Typed value flow (token → `processValue` → converter → typed object, wrapped on failure) | Yes | Candidate lines 31, 64; `Option.java:844-871`, `CommandLine.java:610-624` |
| RF-85 Error flow — parse failures surface as `ParseException` subtypes; the SPI declares only `ParseException` | Yes | Candidate lines 24, 74 (diagram edge) establish the taxonomy; `CommandLineParser.java:32` |
| RF-86 Custom output formats via `HelpAppendable`/`FilterHelpAppendable`; `Xhtml`/`Apt` examples | Yes | Candidate line 48 names both example renderers; `example/XhtmlHelpAppendable.java:32`, `example/AptHelpAppendable.java:34` |
| RF-87 Custom tables via `TableDefinition` + the `getTableDefinition` hook; `WeirdOptionFormat` example | No | Candidate lines 44, 46 cover the hook and the type but never `example/WeirdOptionFormat.java` |
| RF-88 Test packages `cli`, `.bug`, `.example`, `.help` | No | Only `.example` is referenced (line 48); `src/test/java/org/apache/commons/cli/bug/`, `src/test/java/org/apache/commons/cli/help/` uncovered |

**Covered reference facts: 55**
**Total reference facts: 88**

### Recall gaps by theme

The 33 uncovered facts cluster into four groups:

1. **Low-level `Option` semantics (RF-10, 12, 13, 14, 16, 18, 19).** The candidate treats `Option` as an opaque descriptor; arity constants, `acceptsArg()`/`requiresArg()`, value-separator splitting, `getKey()`, the `null`-vs-empty-array contract and the validator's character rules are absent.
2. **Legacy internals (RF-27, 28, 29, 46, 48, 49, 55, 58–59 details, 78, 79, 88).** The deprecated `Parser` subclasses and the deprecated `HelpFormatter` are named but never explained; `Options.addOptions`, `DeprecatedAttributes`, the pattern codes and the one-way constant aliasing are missing.
3. **Help subsystem plumbing (RF-66, 69, 70, 71, 87).** The candidate names `FilterHelpAppendable`, `TextStyle` and `OptionFormatter` as files and conveys their rough role, but never their mechanics — the appendable-delegation contract, the style model, the formatter's presentation defaults, or the custom-table example.
4. **Fine-grained parser policy (RF-37, 43, 45).** `getLongPrefix` scanning, the `checkRequiredArgs` exception with its `-Dflag` exemption, and the `handleProperties` rules (`yes`/`true`/`1`, unknown-key failure, skipping selected groups) are all absent even though the document explicitly walks the parse flow.

---

## Metrics

Computed with `metrics.py` from the `evaluate-docs` skill (`python3 /Users/dariabelll/.config/opencode/skills/evaluate-docs/metrics.py 78 85 55 88`).

```
Precision: 0.9176
Recall:    0.6250
F1:        0.7436
```

| Metric | Value |
|---|---|
| Precision | 0.9176 (78/85) |
| Recall | 0.6250 (55/88) |
| F1 | 0.7436 |

### Summary

Precision is high: the document's architecture, flow, diagram and build-quality claims are almost all confirmed by source. The seven unsupported claims are narrow — two are internal contradictions the document resolves against itself (`requiredOpts` called a map at line 13 but a heterogeneous list at line 80; "nothing in the core model depends on the help subsystem" at line 48 while line 25 admits the reverse dependency), one over-attributes a deprecated-only behaviour (`Option.clearValues` is called only by `Parser`, not `DefaultParser`), one misstates a declaration type (raw `List`, not `List<Object>`), one overstates a count ("~50" overloads vs. 40) and two are loose characterisations (`Option` is mutable; `Option` has no default-value field).

Recall is the weaker axis. The document is accurate about what it covers but thin on mechanism: it names every architectural component while omitting roughly a third of the important behavioural facts — value-separator splitting, the group-selection and required-option bookkeeping details, the `Properties` default-value policy, the legacy `Parser` subclass semantics, and the internals of the pluggable help pipeline (`HelpAppendable`/`TextStyle`/`OptionFormatter` defaults).

---

## Reproducibility notes

- Evidence was gathered only from `src/main/java/org/apache/commons/cli/**`, `src/test/java/org/apache/commons/cli/**`, `pom.xml` and `src/conf/**` at commit `d95484f57dfa4b99ac9069bb3f44df680306e8e9`.
- `README.md`, `RELEASE-NOTES.txt`, `CONTRIBUTING.md`, `src/site/xdoc`, `src/changes` and `pom.xml` javadoc/description prose were **not** used as evidence.
- `reference-facts.md` was created from source and saved before the candidate document was opened, so the recall denominator was not tailored to the candidate.
- Neither `reference-facts.md` nor the candidate document was modified during evaluation; the only repo change is the newly created `reference-facts.md`.
- Metrics were produced by the skill's `metrics.py`, not computed manually.