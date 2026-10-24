import {Languages} from 'lucide-react';
import {languages, useI18n, type Language} from './i18n';

export function LanguageSwitcher(){
  const {language,setLanguage,t}=useI18n();
  return <label className="language-switcher" title={t('Interface language')}>
    <Languages size={16} aria-hidden="true"/>
    <span className="sr-only">{t('Language')}</span>
    <select data-testid="language-select" aria-label={t('Language')} value={language}
      onChange={event=>setLanguage(event.target.value as Language)}>
      {languages.map(option=><option key={option.code} value={option.code} lang={option.code}>{option.name}</option>)}
    </select>
  </label>;
}
