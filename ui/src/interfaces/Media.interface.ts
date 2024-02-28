import type { Version } from "./Version.interface";

export interface Media {
    title: string;
    description: string;
    thumbnail: string;
    uploader: string;
    uploader_id: string;
    duration: number;
    view_count: number;
    was_live: boolean;
    upload_date: string;
    filesize: number;
    ext: string;
    webpage_url: string;

    versions: Version[];
}