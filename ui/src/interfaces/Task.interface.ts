import type { Media } from "./Media.interface"
import type { Preset } from "./Preset.interface"

export enum TaskType {
    Download = "download",
    Import = "import",
    Refresh = "refresh",
    Schedule = "schedule",
    Scan = "scan",
    Rename = "rename",
    Retag = "retag",
}

export enum TaskStatus {
    Pending = "pending",
    Running = "running",
    Finished = "finished",
    Scheduled = "scheduled",
    Failed = "failed",
}

export interface Task {
    id: number,
    priority: number,
    type: TaskType,
    status: TaskStatus,
    when: Date,
    after: number,

    preset_id: string,
    media_id: string,

    media: Media
    preset: Preset
}