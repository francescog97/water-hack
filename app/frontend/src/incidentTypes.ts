export type TaskStatus = 'system_suggested' | 'specialist_approved' | 'in_progress' | 'completed' | 'rejected' | 'blocked';
export interface IncidentSource {id:string;title:string;url?:string|null;path?:string;verification:string;caveats:string;section?:string;retrieved_at?:string;source_classification?:string;}
export interface IncidentTask {id:string;title:string;kind:'verification'|'response';required_for_review:boolean;evidence_required:boolean;proposed_owner_role:string;due_label:string;source_ids:string[];status:TaskStatus;assignee_name?:string|null;assignee_role?:string|null;note?:string|null;evidence_status?:string;internal_target_at?:string|null;}
export interface IncidentScenario {
 id:string;title:string;description:string;mode:string;
 waterbody:{name:string;country:string;geometry_status:string;jurisdiction_status:string};
 observation:{label:string;parameter:string;unit:string;baseline:number;value:number;ratio:number;anomaly_status:string;sample_id:string;observed_at:string;baseline_observed_at:string;mode:string;lab_confirmation:string;confidence:string;threshold:number;threshold_note:string;caveats:string[]};
 receptors:{id:string;name:string;type:string;notes:string;impact:string;source_classification:string}[];
 authorities:{id:string;name:string;role:string;verification:string;jurisdiction_status:string;source_ids:string[]}[];
 legal_checks:{id:string;title:string;notes:string;source_ids:string[];verification:string}[];
 sources:IncidentSource[];tasks:IncidentTask[];limitations:string[];evidence?:Record<string,unknown>;
}
export interface Incident {id:string;scenario:IncidentScenario;revision:number;status:string;review_status:string;tasks:IncidentTask[];reviews:Record<string,unknown>[];timeline:Record<string,unknown>[];outcome:Record<string,unknown>|null;official_authorization:false;dispatch_available:false;}
