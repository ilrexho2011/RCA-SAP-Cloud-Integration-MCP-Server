# Package Name Resolution Fix v2.1.4

This patch corrects cases where `package_name` was incorrectly populated with the technical `package_id` value (for example `FIRST`).

## What changed

- `KnowledgeGenerationService` now resolves package display names from the package catalog returned by `list_packages()`.
- `_collect_iflows()` enriches each iFlow item with `PackageName` when only `PackageId` is present.
- Existing generated interface catalog markdown files were normalized so that:
  - `package_name` contains the business/display package name
  - `* Package:` in the Scope section contains the business/display package name
  - `* Package ID:` remains the technical package ID

## Example

Before:

```md
package_name: "FIRST"
* Package: FIRST
* Package ID: FIRST
```

After:

```md
package_name: "01 - Configurations in Cloud Integration"
* Package: 01 - Configurations in Cloud Integration
* Package ID: FIRST
```
