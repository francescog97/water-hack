import {lazy, Suspense} from 'react';
import NavigatorApp from './NavigatorApp';
import {useI18n} from './i18n';
const App=lazy(()=>import('./App'));

export default function ProductApp(){
 const {t}=useI18n();
 if(new URLSearchParams(window.location.search).get('module')==='flood'){
  const target=new URL(window.location.href);target.searchParams.set('module','pollution');target.hash='';
  return <><div className="legacy-module-banner"><span>{t('Historical flood module')}</span><a href={target.pathname+target.search}>{t('Open pollution navigator')}</a></div><Suspense fallback={<p>{t('Opening the decision navigator…')}</p>}><App/></Suspense></>;
 }
 return <NavigatorApp/>;
}
