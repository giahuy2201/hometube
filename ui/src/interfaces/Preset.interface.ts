export interface Preset {
    id: string;
    description: string;
    download_path: string;
    media_path: string;
    format: string;
    template: string;
    squareCover: boolean;
    addThumbnail: boolean;
    addMetadata: boolean;
    addSubtitles: boolean;
}