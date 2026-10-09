# Documentation Evaluation

## Evaluation metadata

| Field | Value |
|---|---|
| Candidate document | `/Users/dariabelll/Desktop/docs-llm-proj-test/opentelemetry-collector/generated-architecture-ot-space-bunny.md` |
| Candidate SHA-256 | `2ccfcb8a85c00b733b5d88953f94f36c2e4aaae2efd436335910aa70e178096e` |
| Source repository | `/Users/dariabelll/Desktop/docs-llm-proj-test/opentelemetry-collector` |
| Source commit | `7b425533dfa04ff0a0d3b384381979e945a69b2a` (no tracked modifications; untracked files are only the candidate and `reference-facts.md`) |
| Reference facts file | `/Users/dariabelll/Desktop/docs-llm-proj-test/opentelemetry-collector/reference-facts.md` (created from source-code inspection before any candidate document was read) |
| Reference SHA-256 | `83606392010c4b6851776235e7eab39294be594c00ef8fc0c5ee8f39f196c0a2` |
| Generating model | space bunny |
| Evaluator model | MiMo-V2.6-Flash Free |
| Metrics tool | `metrics.py` from the `evaluate-docs` skill |

Notes on inputs:

- The candidate was read in place; neither the candidate nor `reference-facts.md` was modified.
- Evidence comes only from source code, build files, and configuration in the repository at the recorded commit (README/docs/CHANGELOG/AGENTS.md were not used as evidence).

---

## Precision

| Claim | Verdict | Evidence |
|---|---|---|
| C1: Collector core is a telemetry-agnostic routing proxy building a DAG of components and pushing traces/metrics/logs/profiles through it | Supported | `receiver/`, `processor/`, `exporter/`, `connector/` packages; `pipeline/xpipeline/config.go:8` (`SignalProfiles`) |
| C2: Go multi-module monorepo with no `go.work` file | Supported | 100 `go.mod` files under the tree; `ls go.work` → not found |
| C3: "99 separate `go.mod` modules" | Unsupported | Contradicted: `find . -name go.mod` yields 100 files, all `module go.opentelemetry.io/collector...` (99 submodules + root) |
| C4: Coordination through `replace` directives and Make recursion; `Makefile:152-163` fans a target out to every module directory | Supported | `Makefile:153` (`GOMODULES = $(ALL_MODULES) $(PWD)`), `Makefile:163` (`for-all-target: $(GOMODULES)`) |
| C5: Primarily framework/library plus reference server binary `cmd/otelcorecol`; distributions assembled by `cmd/builder` from a manifest | Supported | `cmd/otelcorecol/main.go:1` (builder-generated), `cmd/builder/internal/builder/` |
| C6: Cobra command tree "(`otelcorecol`, `featuregate`, `components`, `validate`, `print`)" | Unsupported | Contradicted: the subcommand is `print-config` (`otelcol/command_print.go:27` `Use: "print-config"`); `otelcol/command.go:77`, `command_components.go:47`, `command_validate.go:15` for the others |
| C7: Reference binary explicitly labelled "testing only" in its `BuildInfo` | Supported | `cmd/otelcorecol/main.go:22` (`Description: "Local OpenTelemetry Collector binary, testing only."`) |
| C8: Key source locations (`main.go`, `components.go`, `command.go`, `flags.go`, `command_print.go`, `command_components.go`, `command_validate.go`) all exist | Supported | all seven files present in `cmd/otelcorecol/` and `otelcol/` |
| C9: `main.go` builds `CollectorSettings` with a `components()` factory and a `ResolverSettings` listing five provider factories, handed to `otelcol.NewCommand` | Supported | `cmd/otelcorecol/main.go:32-36` (env/file/http/https/yaml factories) |
| C10: `NewCommand`'s `RunE` applies CLI flags, calls `NewCollector`, then `col.Run(ctx)` | Supported | `otelcol/command.go:31-41` |
| C11: `main.go`/`components.go` carry the builder `DO NOT EDIT` header and are produced from `builder-config.yaml` by `genotelcorecol` | Supported | `cmd/otelcorecol/main.go:1`, `components.go:1`; `Makefile:176-177` |
| C12: `otelcol/collector.go` owns state machine, pre-logger log buffer, OS signal handling, reload policy, shutdown sequencing | Supported | `otelcol/collector.go`, `otelcol/buffered_core.go`, `otelcol/collector_core.go` |
| C13: Key locations `collector.go`, `configprovider.go`, `config_diff.go`, `redact.go`, `buffered_core.go` exist | Supported | all present |
| C14: Calls `ConfigProvider.Get`/`getWithConf`, `service.New` + `service.Start`/`Shutdown`, `grpclog.SetLogger` | Supported | `otelcol/configprovider.go:56,62`, `otelcol/collector.go:275` |
| C15: Control loop `select` spans `otelcol/collector.go:461-491` | Supported | `LOOP:` at `:461`, `select {` at `:463`, last case at `:486-491` |
| C16: "selects over four channels ...: the config watcher, the component async-error channel, the OS signal channel, and the shutdown channel" | Unsupported | Contradicted: five receive cases — `:464` config watcher, `:472` async error, `:475` signals, `:483` shutdown, `:486` `<-ctx.Done()` |
| C17: confmap loads/merges/expands from URI-scheme providers into one `confmap.Conf`, resolving `${scheme:key}` | Supported | `confmap/resolver.go`, `confmap/expand.go`, `confmap/internal/conf.go` |
| C18: Key locations `resolver.go`, `expand.go`, `internal/conf.go`, `internal/decoder.go`, `validation.go`, `provider.go`, five provider dirs exist | Supported | all present |
| C19: `Resolver.Resolve` retrieves per URI, merges, snapshots pre-expansion copy, expands, then runs `Converter`s | Supported | `confmap/resolver.go:170-194` (retrieve/merge, `unexpandedConfMap` at `:189`), `:194` expand, `:202-203` converters |
| C20: Built on `github.com/knadh/koanf/v2` with `"::"` key delimiter | Supported | `confmap/internal/conf.go:19-20,39`, `confmap/go.mod` (koanf/v2) |
| C21: Turns untyped `Conf` into typed `component.Config` by dispatching to factories, then validates | Supported | `otelcol/internal/configunmarshaler/configs.go:17-59` |
| C22: Key locations incl. `config/` with exactly 12 submodules (list) | Supported | `ls -d config/config*` → 12 dirs matching the listed names |
| C23: `Configs[F].Unmarshal` looks up `factories[id.Type()]`, calls `CreateDefaultConfig()`, decodes `conf.Sub(id.String())` | Supported | `otelcol/internal/configunmarshaler/configs.go:27,47-59` |
| C24: "`confmap/` supplies the decoder; `featuregate/` gates which decode path is taken" | Unsupported | Insufficient/contradicting: the only confmap gate is `confmap.enableMergeAppendOption` used in `Conf.Merge` (`confmap/internal/conf.go:101`); `confmap/metadata.yaml` declares no `feature_gates`, and no gate selects a decode path |
| C25: `service/` façade creates self-telemetry (logger, meter, tracer over shared `pcommon.Resource`), builds graph, manages extensions | Supported | `service/service.go:108-213` (resource `:130`, logger `:150`, meter `:167`, tracer `:182`) |
| C26: Key locations (`service.go` incl. `UpdateReceivers`, `config.go`, `pipelines/config.go`, `extensions/{extensions,graph}.go`, `telemetry/telemetry.go`, `internal/status/`) exist | Supported | `service/service.go:337`, all listed files present |
| C27: Creates the five `service/internal/builders` types, then calls `graph.Build` | Supported | `service/service.go:112-116` (five builders), `:207` (`initGraph`) |
| C28: Delegates `Start`/`Shutdown` to graph and extension manager; reports component status through `componentstatus` | Supported | `service/service.go:232-323`, `:349` (`ReportStatus`) |
| C29: Pipeline graph is gonum-backed, instantiates components, enforces start/shutdown ordering | Supported | `service/internal/graph/graph.go:26-28` (gonum imports), `:406,467` |
| C30: Key locations (`Build`, `createNodes`, `createEdges`, `buildComponents`, `StartAll`, `ShutdownAll`, `UpdateReceivers`, node files, `host.go`, `attribute.go`) correct | Supported | `graph.go:101,268,297,406,467,515`; `{receiver,processor,exporter,connector,capabilities,fanout}.go`, `host.go` present |
| C31: Consumes `service.Settings` + `pipelines.Config`; produces six node types | Supported | `graph.Build` inputs; node types `receiverNode`, `processorNode`, `exporterNode`, `connectorNode`, `capabilitiesNode`, `fanOutNode` |
| C32: "wraps every component with `obsconsumer` / `refconsumer` / `capabilityconsumer` instrumentation" | Unsupported | Contradicted: `refconsumer` only wraps connectors (`service/internal/graph/connector.go:131-152`); `capabilityconsumer` only wraps `capabilitiesNode` (`graph.go:314-340`); receivers get `obsconsumer` + `fanoutconsumer` (`receiver.go:71-93`) |
| C33: Connectors are registered as exporter of one pipeline and receiver of another — the only way pipelines connect | Supported | `service/internal/graph/graph.go:195-197` (same `connNode` in both maps) |
| C34: Consumer plumbing key locations (`consumer/*.go`, `consumer/internal/consumer.go` with `Capabilities`/`MutatesData`, fanoutconsumer files, `consumererror/`) exist | Supported | `consumer/consumer.go:13` (`Capabilities = internal.Capabilities`), all files present |
| C35: "`fanoutconsumer` is inserted by `capabilitiesNode` (multi-exporters) and by `receiverNode`" | Unsupported | Contradicted: fanout nodes insert it (`graph.go:349-367`) and receivers do (`receiver.go:71-93`); `capabilitiesNode` wraps `capabilityconsumer`, not `fanoutconsumer` |
| C36: Partitions consumers by `Capabilities().MutatesData` and deep-clones where sharing would be unsafe | Supported | `internal/fanoutconsumer/traces.go:16-18,39-70` |
| C37: `pipeline/` is a tiny module holding `pipeline.ID` (signal + name) and the signal enum | Supported | `pipeline/pipeline.go`, `pipeline/signal.go`, `pipeline/internal/globalsignal/signal.go` |
| C38: Key locations incl. `pipeline/xpipeline/config.go` (`SignalProfiles`) exist | Supported | `pipeline/xpipeline/config.go:8` |
| C39: `service` depends on `pipeline` one-way | Supported | `pipeline/go.mod` has no `go.opentelemetry.io/collector/service` requirement |
| C40: `pipeline` contains no graph builder, node interfaces, or concurrency helpers; DAG lives in `service/internal/graph` | Supported | `pipeline/` contents are ID/signal + `internal/globalsignal`; no builder/node types |
| C41: `pdata` is the in-memory representation plus proto and JSON codecs | Supported | `pdata/plog/pb.go:10,37` (Proto marshal/unmarshal), `pdata/plog/json.go` |
| C42: pdata key locations (`pcommon` `Resource`/`Value`/`Map`/`Slice`/`Timestamp`, `internal/state.go`, `internal/otelgrpc/encoding.go`, `xpdata/`) exist | Supported | all present |
| C43: All top-level types are `type X internal.XWrapper` structs holding `(orig *, state *State)` | Supported | `pdata/plog/generated_logs.go:21`, `pdata/internal/generated_wrapper_exportlogsservicerequest.go:9-12` |
| C44: Mutation is in place, guarded by a panic-on-read-only assertion | Supported | `pdata/internal/state.go:37-41` |
| C45: Component API key locations (`component.go` `Component`/`Factory`/`Kind`/`StabilityLevel`, `identifiable.go` `Type`/`ID`, `host.go`, `telemetry.go`, `componentstatus/`, per-kind modules, `scraper/`) exist | Supported | `component/component.go:87,107,182`, `component/identifiable.go:131`, all listed packages present |
| C46: Receivers and extensions are components only; processors, exporters, connectors are components *and* consumers | Supported | `receiver/receiver.go:20-22`, `extension/extension.go:16-18`, `processor/processor.go:16-19`, `exporter/exporter.go:16-19`, `connector/connector.go:28-31` |
| C47: Every kind has an `x`-prefixed sibling module (7 listed) holding the experimental Profiles API | Supported | `xreceiver`, `xprocessor`, `xexporter`, `xconnector`, `xextension`, `xconsumer`, `xpipeline` each with own `go.mod` |
| C48: x modules are "exempted from the stability policy" | Supported | `versions.yaml:34-96` (x modules in `beta:` set), `Makefile:281-299` (apidiff runs only for `STABLE_MODULES`) |
| C49: Helper-library key locations (`base_exporter.go`, `queue/{queue,memory_queue,persistent_queue,async_queue}.go`, `queuebatch/`, `processor.go`, `obsreport.go`, `controller.go`) exist | Supported | all present |
| C50: `exporterhelper` is the only helper introducing asynchrony (worker pool + optional persistent store) | Supported | `exporter/exporterhelper/internal/queue/async_queue.go`, `persistent_queue.go`; no goroutines/queue in `processorhelper` |
| C51: `processorhelper` is purely synchronous and in-band | Supported | `processor/processorhelper/processor.go` — no `go func`/`chan`/queue |
| C52: `receiverhelper` is observability only | Supported | `receiver/receiverhelper/obsreport.go` (obs report helpers) |
| C53: `scraperhelper` owns the polling ticker | Supported | `scraper/scraperhelper/controller.go:57-72` (`WithTickerChannel`, `tickerCh`) |
| C54: `featuregate/` is a global runtime-toggleable registry gating behaviour by lifecycle stage | Supported | `featuregate/registry.go`, `featuregate/stage.go` |
| C55: Key locations `registry.go`, `gate.go`, `stage.go`, `flag.go` exist | Supported | all present in `featuregate/` |
| C56: Gates registered at `init()` (mostly via mdatagen-generated `generated_feature_gates.go`), overridable via `--feature-gates` | Supported | `service/internal/metadata/generated_feature_gates.go:1,14`, `featuregate/flag.go` |
| C57: "Four independent generators, each with a Make target and a CI freshness gate" | Supported | `Makefile:104` (`gogenerate`), `:177` (`genotelcorecol`), `:191` (`genpdata`), `:459-471` (`generate-schemas`/`check-schemas`); `.github/workflows/build-and-test.yml:144-157,169` (`git diff --exit-code` gates) |
| C58: Codegen key locations (builder `config/main/templates.go`, mdatagen 5 files, `cfggen/`, `internal/schemagen/{model,schema,resolver}.go`, `cmd/schemagen/internal/parser.go`, `internal/cmd/pdatagen/main.go`, `.mdatagen.yaml`, `.schemagen.yaml`) exist | Supported | all verified present |
| C59: `cmd/builder` consumes a manifest and emits a whole new collector module | Supported | `cmd/builder/internal/builder/main.go`, `templates/` |
| C60: `cmd/mdatagen` emits `internal/metadata/*` plus README fragments | Supported | `cmd/mdatagen/internal/command.go:788-805` (injects config docs into `README.md`) |
| C61: `internal/cmd/pdatagen` emits the entire `pdata` package | Supported | `Makefile:191-193` (`genpdata`), `internal/cmd/pdatagen/` |
| C62: `schemagen` and `internal/schemagen` are two independent JSON-Schema pipelines | Supported | `cmd/schemagen` → `config.schema.yaml` (`Makefile:459-471`), `internal/schemagen/writer.go:15` → `config.schema.json` |
| C63: `main()` builds settings and calls `otelcol.NewCommand(...).Execute()` | Supported | `cmd/otelcorecol/main.go` |
| C64: `updateSettingsUsingFlags` requires ≥1 `--config` URI and ≥1 provider factory; defaults `DefaultScheme` to `"env"` | Supported | `otelcol/command.go:53-73` |
| C65: `configProvider.getWithConf` resolves the config and unmarshals into typed structs | Supported | `otelcol/configprovider.go:62-75` |
| C66: `confmap.Validate(cfg)` walks for `Validate() error` methods; `otelcol.Config.Validate` checks cross-references | Supported | `confmap/validation.go:34-40`; `otelcol/config.go:49,89+` ("references only configured components") |
| C67: Raw pre-decode map is fingerprinted when partial reload is enabled | Supported | `otelcol/collector.go:203-204` (`ReceiverPartialReloadEnabled()` → `fingerprintForPartialReload`) |
| C68: `redactByMirroring` builds a pre-expansion, secret-free view of the config for extensions | Supported | `otelcol/collector.go:219`, `otelcol/redact.go:19-57` |
| C69: `service.New` creates self-telemetry, then the graph, then extensions | Supported | `service/service.go:150` (logger), `:207` (`initGraph`), `:213` (`initExtensions`) |
| C70: Buffered debug logs captured before the real logger existed are flushed through the new core | Supported | `otelcol/collector.go:264-270` (`col.bc.TakeLogs()` written into service logger) |
| C71: `Collector.Run` enters its select loop over signals / watcher / async errors / shutdown | Supported | `otelcol/collector.go:461-491` |
| C72: `createNodes` (`graph.go:101`) and `createEdges` (`graph.go:268`) | Supported | exact line numbers match (`func (g *Graph) createNodes` at `:101`, `createEdges` at `:268`) |
| C73: Chain diagram: receivers → `capabilitiesNode` → processors → `fanOutNode` → exporters (processors chained in declared order) | Supported | `service/internal/graph/graph.go:268-293` |
| C74: Fan-in is implicit — all receivers of a pipeline feed the single `capabilitiesNode` | Supported | `graph.go:271-274` (every receiver → `pg.capabilitiesNode`) |
| C75: `buildComponents` (`graph.go:297`) walks the graph in reverse topological order | Supported | `graph.go:297-303` (`topo.Sort` then `slices.Backward`) |
| C76: For connectors, the same node object is registered in producing exporter map and consuming receiver map (`graph.go:189-198`) | Supported | `graph.go:195-197` (`connNode` assigned to both pipeline maps) |
| C77: No goroutines or channels between graph nodes; data moves by synchronous inline calls on the receiver's goroutine | Supported | fan-out via `fanoutconsumer.New*` calls (`graph.go:349-367`); no `go func`/`chan` in the data path (only `Host.AsyncErrorChannel` for status, not data) |
| C78: `fanoutconsumer` decides per call whether to hand over the original buffer or a deep copy based on `MutatesData` | Supported | `internal/fanoutconsumer/traces.go:39-70` |
| C79: Any asynchrony is inside a component — most commonly the `asyncQueue` worker pool in `exporterhelper` | Supported | `exporter/exporterhelper/internal/queue/async_queue.go` |
| C80: Reload flow: SIGHUP/watcher → re-resolve → fingerprint → `receiversOnlyChanged` (with both gates) → `UpdateReceivers`, else full `service.Shutdown` + rebuild | Supported | `otelcol/collector.go:281-320`, `service/service.go:260-264` |
| C81: `receiversOnlyChanged` (`otelcol/config_diff.go:152`) requires equality of non-receiver hash, extension list, pipeline set, and each pipeline's processors and exporters | Supported | `otelcol/config_diff.go:152-189` (exact conditions at `:153,157,161,171,175`) |
| C82: `UpdateReceivers` (`service/internal/graph/graph.go:515`) runs nine phases and never touches processors, exporters, connectors, or virtual nodes | Supported | `graph.go:515-684` (`// Phase 1..9` comments at `:525,540,555,596,608,631,647,662,684`; all phases only handle receiver nodes) |
| C83: Extensions start in dependency order (`topo.Sort`) and shut down in reverse | Supported | `service/extensions/graph.go:51` (`topo.Sort`), `service/extensions/extensions.go:42` (start forward), `:74` (`slices.Backward` shutdown) |
| C84: Graph components: start reverse topological with receivers forced last; shutdown topological with receivers first | Supported | `graph.go:430-433` (`slices.Backward` start), `:476-478` (forward shutdown) |
| C85: Self-telemetry: logger → meter → tracer on start; tracer → meter → logger on shutdown | Supported | `service/service.go:150,167,182` (creation), `:308-316` (reverse shutdown) |
| C86: "`topo.SortStabilized` uses a comparator that pushes `receiverNode` to the end of the sort" | Unsupported | Contradicted: the comparator returns `-1` when node1 is a receiver, sorting receivers **first** (`service/internal/graph/graph.go:416-422`); receivers start last only because `StartAll` iterates `slices.Backward` (`:430`) |
| C87: "`service/internal/graph`, `internal/fanoutconsumer`, and `service/extensions` contain zero `go func`, channels, or mutexes" | Unsupported | Contradicted: `service/internal/graph/host.go:32` declares `AsyncErrorChannel chan error` (fed by `NotifyComponentStatusChange`, `host.go:101-105`) |
| C88: The only exception is the per-`InstanceID` lock in `service/internal/status` | Supported | `service/internal/status/status.go:112` (`mu sync.Mutex`); no other `sync.Mutex`/`chan` in the three named packages |
| C89: Components own their own concurrency per the contract documented on `component.Component.Start` | Supported | `component/component.go:32-37` (background operations / own context) |
| C90: Receivers/exporters keyed by fnv64a hash of their attribute set (`service/internal/attribute/attribute.go:27`), existing node reused | Supported | `service/internal/attribute/attribute.go:27-32` (`fnv.New64a()`), node reuse in `graph.go:216-251` |
| C91: Processors keyed by `(pipelineID, componentID)`; config validation rejects duplicate processors in one pipeline | Supported | `service/internal/graph/processor.go:36-41`, `service/pipelines/config.go:68-71` |
| C92: Processors form a chain (slice order = execution order); every receiver feeds every processor; no sub-chain routing | Supported | `PipelineConfig.Processors` slice + `graph.go:275-282` chaining |
| C93: `pdata` `State` carries a read-only bit; setters call `AssertMutable()` and panic with `"invalid access to shared data"` | Supported | `pdata/internal/state.go:37-41` |
| C94: `fanoutconsumer` deep-copies for all but the last mutating consumer and calls `MarkReadOnly()` when more than one read-only consumer sees the object | Supported | `internal/fanoutconsumer/traces.go:51-70` |
| C95: `confmap/internal/decoder.go:55` sets `ErrorUnused: !IgnoreUnused`; `MatchName: caseSensitiveMatchName` overrides case-insensitive matching | Supported | `confmap/internal/decoder.go:55,59,394-397` |
| C96: Squashed embedded structs sharing a `Conf` must opt out with `confmap.WithIgnoreUnused()` | Supported | `confmap/internal/decoder.go:278` comment |
| C97: Two-phase decode: first `map[component.ID]map[string]any` (keys through `component.ID.UnmarshalText`, duplicate-after-normalisation rejected), then `conf.Sub(id.String())` preserving `ExpandedValue` | Supported | `configs.go:27,42-43` ("preserve internal representation"), `component/identifiable.go:131`, `configs_test.go:110-115` ("duplicate name") |
| C98: No built-in provider supports watching (all five discard `WatcherFunc`); reload is SIGHUP-only; http/https configure no auth and no client timeouts | Supported | `confmap/provider/{env,file,yaml}provider/provider.go:47,45,37`, `configurablehttpprovider/provider.go:49,67,80`, `otelcol/collector.go:450` (SIGHUP) |
| C99: Gate stages determine defaults (Alpha/Deprecated off, Beta/Stable on); Stable cannot be disabled and Deprecated cannot be enabled (errors); `ReceiverPartialReloadEnabled()` requires both gates | Supported | `featuregate/stage.go`, `featuregate/registry.go:184-193`, `service/service.go:260-264`, `generated_feature_gates.go:18,26` (Alpha/Beta) |
| C100: Extensions get a `ConfigSnapshot` whose `Unexpanded()` redacts `configopaque` leaves but keeps exact `${...}` references (`otelcol/redact.go:22`); reload fingerprints the raw pre-decode map | Supported | `extension/extensioncapabilities/interfaces.go:43-51`, `otelcol/redact.go:22,57`, `otelcol/collector.go:343` (`fingerprintForPartialReload(rawConf, ...)`) |
| C101: Partial reload is fail-fast (first error returns, possibly leaving the graph partially modified) and `otelcol` then discards the service and rebuilds | Supported | `service/internal/graph/graph.go:596-607` (immediate `return err`), `otelcol/collector.go:296-320` |
| C102: "The two `*bool`/`error` return values of `tryPartialReceiverReload`" | Unsupported | Contradicted: signature is `(bool, error)` — `otelcol/collector.go:328` |
| C103: `cmd/schemagen` is AST-based (`go/ast` + `go/packages`), reads `mapstructure` tags and doc comments, and has no dependency on the shared module | Supported | `cmd/schemagen/internal/ast_helpers.go:91-96`, `parser.go:310`, `cmd/schemagen/go.mod` (no collector-internal requires) |
| C104: `internal/schemagen` is metadata-driven (reads the `config:` block) consumed via an alias-only facade, and emits both JSON Schema and Go structs | Supported | `cmd/mdatagen/internal/cfggen/shared_alias.go:6,67` (type aliases + `WriteJSONSchema`), `internal/schemagen/model.go:72` (`mapstructure:"config"`), `cmd/mdatagen/internal/command.go:758,772` (`config.schema.json` + `generated_config.go`), `internal/schemagen/writer.go:15` |
| C105: `internal/cmd/pdatagen` emits public wrappers and hand-rolled gogo-style wire codecs from a schema expressed as Go structs with hand-assigned field numbers | Supported | `internal/cmd/pdatagen/internal/pdata/*.go` (`protoID: 1` etc., `MessageField.protoID`), `internal/proto/field.go:233` (`genProtoTag`), `pdata/internal/generated_proto_*.go` (`MarshalProto`) |
| C106: The only `.proto` files in the tree are the exporter queue metadata and the `xpdata` request envelope | Supported | `find . -name '*.proto'` → `exporter/exporterhelper/internal/queue/meta.proto`, `pdata/xpdata/request/internal/request.proto` |
| C107: "`google.golang.org/protobuf` and the upstream OTLP protos appear only in tests" | Unsupported | Contradicted by production imports: `exporter/exporterhelper/internal/queue/persistent_queue.go:15`, `receiver/otlpreceiver/encoder.go:8-9`, `exporter/otlphttpexporter/otlp.go:20` |
| C108: x modules are separate modules, not build-tagged files; no `//go:build` tags and no `Deprecated:` markers | Supported | grep over all seven x modules returns no `//go:build` and no `Deprecated:` |
| C109: `builder-config.yaml` carries 82 `replace` directives; `default.yaml` derived by a `sed` rule at `cmd/builder/Makefile:19` | Supported | `grep -c "^replace " cmd/otelcorecol/go.mod` → 82; `cmd/builder/Makefile:19` (sed removing the `replaces:` stanza) |
| C110: `Component`/`component.Factory` are unsealed (no unexported marker) while per-kind factories add `unexportedFactoryFunc()`; `componenttest.CheckConfigStruct` is a reflective `mapstructure`-tag linter | Supported | `component/component.go:182-194`, `receiver/receiver.go:90`, `component/componenttest/configtest.go:24-35,64-95` |

Supported claims: 100
Total claims: 110

---

## Recall

| Reference fact | Covered | Evidence (candidate section / claim) |
|---|---|---|
| F1: `otelcol.Collector` top-level runtime; `Run` control loop over watch/signals/async errors/shutdown/ctx | Yes | §Collector lifecycle Interactions (C14, C15, C16); §Startup step 4 (C71); reload diagram (C80) |
| F2: Collector states `Starting`/`Running`/`Closing`/`Closed` | No | Only the type name `State` appears in a source-location list; the four states, `atomic.Int64`, and `setCollectorState` are never described |
| F3: `ConfigProvider` wraps `confmap.Resolver`; resolve then unmarshal with factories | Yes | §Collector lifecycle (C14); §Startup step 3.1 (C65) |
| F4: `Resolver.Resolve`: retrieve → merge → pre-expansion snapshot → expand → converters | Yes | §Configuration resolution Interactions (C19) |
| F5: Providers keyed by unique scheme; `DefaultScheme` must exist; `otelcorecol` registers env/file/http/https/yaml | Yes | §Entry point five provider factories (C9); `DefaultScheme` env (C64); provider dirs listed (C18) |
| F6: `Resolver.Watch()`/`ConfigProvider.Watch()` drives reload in `Run` | Yes | §Collector lifecycle "config watcher" channel (C16); reload diagram watcher node (C80); Gotcha 7 (C98) |
| F7: Full reload vs gated partial receiver reload with fallback to full reload | Yes | reload diagram (C80); Gotcha 8 gates (C99); Gotcha 10 fallback (C101) |
| F8: `service.New`: host builders, telemetry resource/logger/meter/tracer, `initGraph`, `initExtensions`, process metrics | Yes | §Service Purpose/Interactions (C25-C27); §Startup step 5 (C69); process-metrics detail omitted |
| F9: `Service.Start` order (extensions → snapshot → pipelines → ready) | No | `Start` appears only as a method name in a source-location list; the startup sequence (extensions first, config-snapshot notification, `PipelineWatcher.Ready`) is never described |
| F10: `Service.Shutdown` order (not ready → pipelines → extensions → telemetry providers) | Yes | §Shutdown ordering table (C83-C85) |
| F11: `graph.Build` creates nodes, edges, instantiates components | Yes | §Pipeline construction (C72, C75); §Pipeline graph (C29-C31) |
| F12: Per-pipeline structure receivers → capabilities → processors → fanout → exporters | Yes | chain diagram (C73); `createEdges` evidence (C74, C76) |
| F13: Capabilities node aggregates `MutatesData`, wraps with `capabilityconsumer` | Yes | §Pipeline graph (C31, C32 — mentions `capabilitiesNode`/`capabilityconsumer`; the aggregation rule itself is not spelled out) |
| F14: `fanoutconsumer` clone/share semantics | Yes | §Consumer plumbing (C36); Telemetry data flow (C78); Gotcha 4 (C94) |
| F15: Build-time topological ordering (`topo.Sort`) and cycle detection | Yes | `buildComponents` reverse topological (C75); cycle-error detail omitted |
| F16: Topological start (downstream first, receivers last) and topological shutdown | Yes | §Shutdown ordering table (C84); receiver-last explanation attempt (C86) |
| F17: Connectors bridge pipelines (wired into both sides) | Yes | §Pipeline graph (C33); `graph.go:189-198` (C76); signal-compatibility validation omitted |
| F18: Receiver/exporter node dedup across pipelines | Yes | Gotcha 2 (C90) |
| F19: `component.Component` lifecycle Start/Shutdown | Yes | §Component API (C45); Gotcha 1/15 (C89, C110) |
| F20: Base factory + kind-specific factories with signal `Create*` and stability getters | Yes | §Component API (C45); Gotcha 15 unexported marker (C110) |
| F21: Stability levels `Undefined`…`Stable` | No | Only the type name `StabilityLevel` is listed; the seven level constants are never enumerated (feature-gate stages are listed, which is a different concept) |
| F22: `graph.Host` + `AsyncErrorChannel` for fatal errors terminating the control loop | Yes | §Collector lifecycle "component async-error channel" (C16); `host.go` listed (C30); Gotcha 1 cites the channel while claiming the opposite (C87) |
| F23: Status reporting during start/stop via `Reporter`/status machinery | Yes | §Service Interactions "reports component status through `componentstatus`" (C28); `service/internal/status/` listed (C26) |
| F24: Extension start order from declared dependencies; reverse shutdown | Yes | §Shutdown ordering table row 1 (C83) |
| F25: Pipeline config validation rules (≥1 pipeline unless gate, ≥1 receiver/exporter, no duplicate processors, profiles gate) | No | Only the duplicate-processor rule is mentioned (C91); the remaining rules from `service/pipelines/config.go:20-75` are absent; the candidate instead describes reference checking in `Config.Validate` (C66) |
| F26: `featuregate` registry, stages, `--feature-gates` flag, defaults by stage | Yes | §Feature gates (C54-C56); Gotcha 8 (C99) |
| F27: `otelcol.NewCommand` with components/validate/print-config/featuregate subcommands | Yes | §Entry point command tree (C6) — covered though the print subcommand is misnamed (see C6); (C10) |
| F28: Builders create components from config+factory maps | Yes | §Service "five `service/internal/builders` types" (C27) |
| F29: `sharedcomponent` deduplicates instances keyed by config | No | Not mentioned anywhere in the candidate (receiver sharing is explained via graph-node dedup, a different mechanism) |
| F30: pdata signals traces/metrics/logs/profiles | Yes | Overview (C1); §Data model (C41-C44) |
| F31: In-tree components (otlpreceiver, batch, memory limiter, queue-batch, forward, debug, zpages) | No | No concrete in-tree component is named anywhere in the candidate (`otlpreceiver`, `batchprocessor`, `debugexporter` — 0 occurrences) |
| F32: `cmd/otelcorecol` is a generated binary from `cmd/builder` | Yes | §Entry point Note (C11); Gotcha 14 (C109) |
| F33: `versions.yaml` stable (v1.x) vs beta (v0.x) module sets | No | `versions.yaml` is never mentioned; module stability is only discussed abstractly via the x-module/apidiff boundary (C48, C108) |
| F34: `Run` registers SIGHUP always / SIGINT+SIGTERM unless disabled; `Shutdown` waits for `Run` cleanup | Yes | §Collector lifecycle OS signal handling (C12); reload diagram SIGHUP (C80); Gotcha 7 "SIGHUP-only" (C98); `WaitGroup` detail omitted |

Covered reference facts: 27
Total reference facts: 34

---

## Metrics

```
Precision: 0.9091
Recall:    0.7941
F1:        0.8477
```

(Computed with `metrics.py` from the `evaluate-docs` skill: `python3 metrics.py 100 110 27 34`.)

Summary of the ten unsupported claims: C3 (module count 99 vs 100), C6 (`print` vs `print-config`), C16 (four vs five select cases), C24 (no feature gate selects a decode path), C32/C35 (`capabilityconsumer`/`fanoutconsumer` wiring misattributed), C86 (comparator puts receivers first, not last), C87 (`chan error` in `graph/host.go`), C102 (`(bool, error)` not `(*bool, error)`), C107 (`google.golang.org/protobuf` used in production code).
