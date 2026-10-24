import {useSyncExternalStore, type ReactNode} from 'react';
import it from './locales/it.json';
import ru from './locales/ru.json';
import bg from './locales/bg.json';

export type Language = 'en' | 'it' | 'ru' | 'bg';
export const languages: {code:Language; name:string}[] = [
  {code:'en',name:'English'}, {code:'it',name:'Italiano'},
  {code:'ru',name:'Русский'}, {code:'bg',name:'Български'},
];
const dictionaries: Record<Exclude<Language,'en'>,Record<string,string>> = {it,ru,bg};
const localeNames:Record<Language,string> = {en:'en-GB',it:'it-IT',ru:'ru-RU',bg:'bg-BG'};
const key = 'crisis2action.language';
const supported = (value:string|null): value is Language => languages.some(language=>language.code===value);
function initialLanguage():Language {
  if (typeof window === 'undefined') return 'en';
  const query = new URLSearchParams(window.location.search).get('lang');
  if (supported(query)) return query;
  try { const saved=window.localStorage.getItem(key); if(supported(saved))return saved; }
  catch { /* Language selection also works when storage is unavailable. */ }
  return 'en';
}
let current = initialLanguage();
const listeners = new Set<()=>void>();
if (typeof document !== 'undefined') document.documentElement.lang = current;
export function getLanguage(){return current;}
export function locale(){return localeNames[current];}
export function setLanguage(language:Language){
  if (!supported(language)) return;
  current=language;
  document.documentElement.lang=language;
  try {window.localStorage.setItem(key,language);} catch { /* Session preference is retained in memory. */ }
  // A query override is only an initial choice; keep a shared URL in sync.
  const url = new URL(window.location.href);
  if(url.searchParams.has('lang')) {url.searchParams.set('lang',language);window.history.replaceState(null,'',url);}
  listeners.forEach(listener=>listener());
}
export function translate(text:string):string {
  if(current==='en'||!text)return text;
  const normalized=text.replace(/\s+/g,' ').trim();
  let translated=dictionaries[current][normalized];
  const day=normalized.match(/^Day \+(\d+)$/);
  if(!translated && day && dictionaries[current]['Day +{days}']) {
    translated=dictionaries[current]['Day +{days}'].replace('{days}',day[1]);
  }
  if(!translated)return text;
  return (/^\s/.test(text)?' ':'')+translated+(/\s$/.test(text)?' ':'');
}
function translateNode(value:ReactNode):ReactNode {
  if(typeof value==='string')return translate(value);
  if(Array.isArray(value))return value.map(translateNode);
  return value;
}
function subscribe(listener:()=>void){listeners.add(listener);return()=>{listeners.delete(listener);};}
export function useI18n(){
  const language=useSyncExternalStore(subscribe,getLanguage,()=> 'en' as Language);
  return {language,setLanguage,t:translate,tx:translateNode,locale:localeNames[language]};
}
