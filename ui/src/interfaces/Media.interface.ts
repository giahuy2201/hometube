import type { Channel } from "./Channel.interface";
import type { Version } from "./Version.interface";

export interface Media {
    id: string;
    title: string;
    description: string;
    thumbnail: string;
    duration: number;
    view_count: number;
    was_live: boolean;
    upload_date: string;
    filesize: number;
    ext: string;
    webpage_url: string;

    channel_id: string;
    uploader: string;
    uploader_id: string;

    channel: Channel;
    versions: Version[];
}