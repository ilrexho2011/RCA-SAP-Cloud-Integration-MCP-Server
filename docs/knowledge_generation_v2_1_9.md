# Knowledge generation v2.1.9

This release strengthens the professional generation and update of KEDB and Runbook artifacts without removing the functional layers added in v2.1.8.

## Main improvements

1. The KEDB and Runbook generation flow now pulls richer context from:
   - `resources/policies`
   - `resources/examples/interface_catalog_docs`
   - `resources/reference_materials/sap-ci-design-and-configuration-inventory`
   - `resources/reference_materials/mpl`
   - `resources/reference_materials/additional_samples`
2. Metadata completion was hardened so that package name, interface ID, iFlow ID, and iFlow name are resolved from local inventory or interface catalog documents whenever possible.
3. MPL evidence is now injected more concretely into generated and updated artifacts, including timestamp, MessageGuid, interface, sender, receiver, and cleaned error text.
4. The OpenAI refinement prompt was upgraded to use the policy files plus the packaged sample KEDB/Runbook models, so the final phrasing becomes more action-led and closer to the approved enterprise style.
5. Local-only fallback generation is stronger: if live tenant content is not available, the service can still infer usable scenario context from interface catalog documents and local design inventory.

## Practical result

The generated KEDB and Runbook documents are now more likely to:
- avoid undefined metadata values,
- expose concrete runtime evidence,
- preserve normalized taxonomy formatting,
- and express diagnosis and recovery steps in short action-led language.
