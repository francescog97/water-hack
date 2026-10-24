import {useI18n, locale, translate} from './i18n';
import type { ReactNode } from 'react';
import { Area, CartesianGrid, ComposedChart, Line, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { ArrowUpRight, Check, ChevronRight, ExternalLink, FileSearch, ShieldCheck, X } from 'lucide-react';
import type { Band, Evaluation, LegalSource, RulePack } from './types';
export function dateLabel(value: string) { return new Intl.DateTimeFormat(locale(), { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(value.slice(0, 10) + 'T12:00:00Z')); }
export function number(value: number | null | undefined, digits = 3) { return value == null ? translate('Unavailable') : value.toLocaleString(locale(), { maximumFractionDigits: digits }); }
export function human(value: string) { const translated = translate(value); return translated === value ? translate(value.toLowerCase().replaceAll('_', ' ')) : translated; }
export function Badge({ children, tone = "neutral" }: {
    children: ReactNode;
    tone?: string;
}) { const { tx: txUi } = useI18n(); return <span className={`badge ${tone}`}>{txUi(children)}</span>; }
export function Panel({ children, title, kicker, aside, className = "" }: {
    children: ReactNode;
    title?: string;
    kicker?: string;
    aside?: ReactNode;
    className?: string;
}) { const { tx: txUi } = useI18n(); return <section className={`panel ${className}`}>{txUi(title && <div className={`panel-head`}><div>{txUi(kicker && <div className={`eyebrow`}>{txUi(kicker)}</div>)}<h2>{txUi(title)}</h2></div>{txUi(aside)}</div>)}{txUi(children)}</section>; }
export function BandBadge({ band }: {
    band: Band;
}) { const { tx: txUi } = useI18n(); return <Badge tone={band.toLowerCase()}><span className={`status-dot`}/>{txUi(band)}</Badge>; }
export function RiskBands({ pack, band }: {
    pack: RulePack;
    band: Band;
}) { const { t: tUi, tx: txUi } = useI18n(); return <div className={`risk-bands`} aria-label={tUi(`Illustrative thresholds`)}>{txUi(([`WARNING`, `DANGER`, `EMERGENCY`] as const).map(n => <div key={n} className={`${n.toLowerCase()} ${band === n ? `active` : ``}`}><span>{txUi(n)}</span><strong>{txUi(`≥ `)}{txUi(pack.thresholds[n])}{txUi(` `)}<small>{txUi(`m³/s`)}</small></strong>{txUi(band === n && <span className={`band-selected`}>{txUi(`Current demo band`)}</span>)}</div>))}<p className={`risk-caption`}>{txUi(`DEMO RISK RULE · not an official warning regime`)}</p></div>; }
export function FlowDiagram({ value, band }: {
    value: number | null;
    band: Band;
}) { const { t: tUi, tx: txUi } = useI18n(); const width = value == null ? 5 : Math.min(46, 10 + value * .6); return <div className={`flow-diagram`}><svg viewBox={`0 0 460 205`} role={`img`} aria-label={tUi(`Conceptual river-flow diagram; no geographic or water-level model`)}><defs><linearGradient id={`riverColor`} x1={`0`} y1={`0`} x2={`1`} y2={`0`}><stop stopColor={`#b8e4e1`}/><stop offset={`1`} stopColor={`#167e89`}/></linearGradient><pattern id={`terrain`} width={`24`} height={`24`} patternUnits={`userSpaceOnUse`}><path d={`M0 24L24 0`} stroke={`#d9e6df`} strokeWidth={`.7`}/></pattern></defs><rect width={`460`} height={`205`} rx={`14`} fill={`#eff5f0`}/><rect width={`460`} height={`205`} rx={`14`} fill={`url(#terrain)`}/><path d={`M-20 150C80 185 90 23 190 70S280 182 355 103S420 20 485 55`} stroke={`#d3e2d7`} fill={`none`} strokeWidth={`70`}/><path d={`M-20 150C80 185 90 23 190 70S280 182 355 103S420 20 485 55`} stroke={`url(#riverColor)`} fill={`none`} strokeWidth={width} className={`river-path`}/><path d={`M-20 150C80 185 90 23 190 70S280 182 355 103S420 20 485 55`} stroke={`#fff`} strokeOpacity={`.7`} fill={`none`} strokeWidth={`2`} strokeDasharray={`7 13`} className={value == null ? `` : `flow-dashes`}/><circle cx={`230`} cy={`100`} r={`23`} fill={`#fff`} stroke={`#b8d3cd`}/><path d={`M221 105V93m9 17V89m9 16V95`} stroke={`#157780`} strokeWidth={`3`} strokeLinecap={`round`}/><rect x={`18`} y={`16`} width={`135`} height={`27`} rx={`6`} fill={`white`}/><text x={`29`} y={`34`} fill={`#42625c`} fontSize={`10`} fontFamily={`sans-serif`}>{txUi(`CONCEPTUAL FLOW`)}</text><rect x={`277`} y={`158`} width={`165`} height={`30`} rx={`7`} fill={`white`}/><text x={`288`} y={`178`} fill={`#244a47`} fontSize={`11`} fontFamily={`sans-serif`}>{txUi(band)}{txUi(` · `)}{txUi(value == null ? `input unavailable` : `${number(value)} m³/s`)}</text></svg><span>{txUi(`Conceptual illustration · no map, water level or inundation model`)}</span></div>; }
export function DischargeChart({ data, compact = false }: {
    data: Evaluation;
    compact?: boolean;
}) { const { tx: txUi } = useI18n(); const history = data.historical_timeline.slice(compact ? -25 : -55); const points: {
    date: string;
    observed: number | null;
    scenario: number | null;
}[] = history.map(p => ({ date: p.date, observed: p.value, scenario: null })); if (data.simulation.length && points.length)
    points[points.length - 1].scenario = data.observation?.value ?? null; for (const p of data.simulation)
    points.push({ date: p.date, observed: null, scenario: p.value }); const max = Math.max(data.rule_pack.thresholds.EMERGENCY * 1.12, ...points.flatMap(p => [p.observed ?? 0, p.scenario ?? 0])) * 1.08; return <div className={`chart-wrap`} data-testid={`discharge-chart`}><div className={`chart-legend`}><span><i className={`line-key`}/>{txUi(`Historical measurement`)}</span><span><i className={`line-key dashed`}/>{txUi(`Synthetic what-if`)}</span><small>{txUi(`Discharge · m³/s`)}</small></div><ResponsiveContainer width={`100%`} height={compact ? 245 : 310}><ComposedChart data={points} margin={{ top: 20, right: 28, left: 0, bottom: 5 }}><defs><linearGradient id={`areaFill`} x1={`0`} y1={`0`} x2={`0`} y2={`1`}><stop offset={`0`} stopColor={`#269398`} stopOpacity={`.18`}/><stop offset={`1`} stopColor={`#269398`} stopOpacity={`0`}/></linearGradient></defs><CartesianGrid stroke={`#e8eeec`} vertical={!1}/><XAxis dataKey={`date`} minTickGap={35} tickLine={!1} axisLine={!1} tick={{ fill: `#71857f`, fontSize: 11 }} tickFormatter={e => new Intl.DateTimeFormat(locale(), {day:"numeric",month:"short",timeZone:"UTC"}).format(new Date(String(e).slice(0,10)+"T12:00:00Z"))}/><YAxis domain={[0, Math.ceil(max)]} width={42} tickLine={!1} axisLine={!1} tick={{ fill: `#71857f`, fontSize: 11 }}/><Tooltip labelFormatter={e => dateLabel(String(e))} formatter={(e, t) => [`${number(Number(e))} m³/s`, t === `observed` ? translate(`Historical measurement`) : translate(`Synthetic what-if`)]} contentStyle={{ borderRadius: 12, border: `1px solid #d8e3df`, fontSize: 12 }}/>{txUi(Object.entries(data.rule_pack.thresholds).map(([e, t]) => <ReferenceLine key={e} y={t} stroke={e === `EMERGENCY` ? `#c07777` : e === `DANGER` ? `#ca9655` : `#c4b767`} strokeDasharray={`3 5`} strokeOpacity={`.7`}/>))}<Area type={`linear`} dataKey={`observed`} stroke={`#188189`} strokeWidth={2.4} fill={`url(#areaFill)`} connectNulls={!1} isAnimationActive={!1}/><Line type={`linear`} dataKey={`scenario`} stroke={`#d38a35`} strokeWidth={2.6} strokeDasharray={`7 5`} dot={{ r: 4, fill: `#fff`, strokeWidth: 2 }} connectNulls={!1} isAnimationActive={!1}/></ComposedChart></ResponsiveContainer><div className={`chart-foot`}><span>{txUi(`Blank dates remain gaps. No interpolation.`)}</span><span>{txUi(data.simulation.length ? `Dashed values are simulated, not a forecast.` : `History shown only through the selected date.`)}</span></div></div>; }
export function SourceLink({ source, onInspect }: {
    source: LegalSource;
    onInspect: (source: LegalSource) => void;
}) { const { tx: txUi } = useI18n(); return <button className={`source-link`} onClick={() => onInspect(source)}><FileSearch size={14}/><span>{txUi(source.publisher)}{txUi(` · `)}{txUi(source.article_or_section)}</span><ChevronRight size={14}/></button>; }
export function SourceDrawer({ source, onClose }: {
    source: LegalSource | null;
    onClose: () => void;
}) { const { t: tUi, tx: txUi } = useI18n(); return source ? <div className={`drawer-backdrop`} onClick={onClose}><aside className={`source-drawer`} role={`dialog`} aria-modal={`true`} aria-label={tUi(`Source evidence`)} onClick={e => e.stopPropagation()}><div className={`drawer-top`}><span className={`eyebrow`}>{txUi(`EVIDENCE RECORD`)}</span><button className={`icon-button`} aria-label={tUi(`Close evidence`)} onClick={onClose}><X size={20}/></button></div><FileSearch className={`drawer-icon`} size={30}/><h2>{txUi(source.source_title)}</h2><Badge tone={`amber`}>{txUi(`Source found · interpretation unreviewed`)}</Badge><p className={`source-summary`}>{txUi(source.paraphrase)}</p><dl className={`evidence-list`}><dt>{txUi(`Publisher`)}</dt><dd>{txUi(source.publisher)}</dd><dt>{txUi(`Section / provision`)}</dt><dd>{txUi(source.article_or_section)}</dd><dt>{txUi(`Version / currency`)}</dt><dd>{txUi(source.version_or_last_verified)}</dd><dt>{txUi(`Retrieved`)}</dt><dd>{txUi(source.retrieved_at)}</dd><dt>{txUi(`Translation`)}</dt><dd>{txUi(source.translation_status)}</dd><dt>{txUi(`Effective version for event`)}</dt><dd>{txUi(source.effective_date_from ?? `Not independently verified`)}</dd><dt>{txUi(`Domain expert`)}</dt><dd>{txUi(source.reviewer ?? `Not reviewed`)}</dd></dl><div className={`callout amber`}><ShieldCheck size={18}/><p>{txUi(source.scope_note)}</p></div><a className={`button primary full`} href={source.official_url} target={`_blank`} rel={`noreferrer`}>{txUi(`Open original source `)}<ExternalLink size={16}/></a><p className={`tiny muted`}>{txUi(`The source link opens externally. Decision support works offline; opening the original requires a connection.`)}</p><button className={`button subtle full`} onClick={onClose}>{txUi(`Return to workspace `)}<Check size={15}/></button></aside></div> : null; }
export function Stat({ label, value, detail, icon }: {
    label: string;
    value: ReactNode;
    detail: string;
    icon?: ReactNode;
}) { const { tx: txUi } = useI18n(); return <div className={`stat-card`}><div className={`stat-label`}>{txUi(label)}{txUi(icon ?? <ArrowUpRight size={15}/>)}</div><div className={`stat-value`}>{txUi(value)}</div><p>{txUi(detail)}</p></div>; }
