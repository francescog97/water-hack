# Interface languages

The header language selector offers **English, Italiano, Русский and Български**. It remains visible while scrolling, including on mobile. English is the default when no preference exists. The choice is saved in this browser under `crisis2action.language`; an optional `?lang=en|it|ru|bg` query sets the initial language of a shared link.

Language changes update navigation, interface labels, guided demo, warning/status labels, review instructions and dialogs. Dates and displayed decimal separators follow the selected locale. Source bytes, timestamps, values, units, station IDs, rule/legal IDs and context fingerprints are unchanged. Switching language does not submit a new evaluation, clear an acknowledgement or reset scenario controls.

Original source titles, evidence text, legal documents, raw JSON and exported incident briefings retain their original language. A translated-interface notice makes this explicit. The interface translations are not expert-verified legal translations and do not change the review status of any source or interpretation. Drafts continue to contain the original English evidence and caveats.

Implementation: `app/frontend/src/i18n.ts`, `LanguageSwitcher.tsx`, and flat locale JSONs in `app/frontend/src/locales/`. Add or change a user-facing English key consistently in each locale; retain an English fallback for missing entries. The switch uses native language names so it remains identifiable in every language. Storage failures retain a session-only choice.

Validation: `npm run typecheck`, `npm run lint`, `npm run build` and all **6 browser tests** passed. The two language tests cover all four choices, document language, preference persistence, unchanged scenario/evaluation/review, localized decimals, original evidence URLs/text and a visible selector without horizontal overflow at 390px. The four existing end-to-end tests still validate the full historical-to-draft workflow.

Changing the interface language does not change Cloudflare Access login policy or the authorized email list. Deployment remains `npm run cloud:deploy:gateway` after build and tests; no backend/schema deployment is required for translations alone.
