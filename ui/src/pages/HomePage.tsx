import React from "react";
import Typography from "@mui/material/Typography";
import Layout from "../components/Layout";
import {
    FormGroup,
    TextField,
    Button,
    Stack,
    MenuItem,
    Select,
    Container,
    SelectChangeEvent,
    Box,
} from "@mui/material";
import LinearProgress from "@mui/material/LinearProgress";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2
import Thumbnail from "../components/Thumbnail";
import axios from "axios";

export default function HomePage() {
    const [url, setURL] = React.useState("");
    const [preset, setPreset] = React.useState("bestvideo");
    const [progress, setProgress] = React.useState(10);
    const [downloading, setDownloading] = React.useState(false);
    const [videos, setVideos] = React.useState<any>([]);

    React.useEffect(() => {
        axios.get("http://localhost:8000/videos").then((res) => {
            setVideos(res["data"]);
        });
    }, [progress]); // This empty array represents an empty list of dependencies

    const updateURL = (event: React.ChangeEvent<HTMLInputElement>) => {
        setURL(event.target.value);
    };

    const updatePreset = (event: SelectChangeEvent) => {
        setPreset(event.target.value);
    };

    const submitRequest = async () => {
        console.log(preset);
        setDownloading(true);
        setProgress(50);
        const result = await axios.post("http://localhost:8000/add", {
            url: url,
            preset: preset,
        });
        // setDownloading(false)
        console.log(result);
        if (result.status == 200) {
            setProgress(100);
        }
    };

    return (
        <Layout>
            <Stack
                sx={{ my: 3 }}
                direction="column"
                spacing={2}
                justifyContent="flex-start"
                alignItems="stretch"
                flexWrap="nowrap"
            >
                <Container>
                    <Stack
                        sx={{ my: 3 }}
                        direction="row"
                        spacing={2}
                        justifyContent="center"
                        alignItems="stretch"
                        flexWrap="nowrap"
                    >
                        <TextField
                            sx={{ display: "flex" }}
                            id="outlined-basic"
                            label="URL"
                            variant="outlined"
                            onChange={updateURL}
                            fullWidth
                        />
                        <Stack
                            direction="row"
                            spacing={2}
                            justifyContent="center"
                            alignItems="stretch"
                            flexWrap="nowrap"
                        >
                            <Select
                                labelId="demo-select-small-label"
                                id="demo-select-small"
                                label="Age"
                                value={preset}
                                onChange={updatePreset}
                            >
                                <MenuItem value={"bestvideo"}>
                                    bestvideo
                                </MenuItem>
                                <MenuItem value={"bestaudio"}>
                                    bestaudio
                                </MenuItem>
                                <MenuItem value={"new"}>
                                    <em>New preset</em>
                                </MenuItem>
                            </Select>
                            <Button variant="contained" onClick={submitRequest}>
                                Download
                            </Button>
                        </Stack>
                    </Stack>
                    {downloading && (
                        <Box sx={{ width: "100%" }}>
                            <Box sx={{ display: "flex", alignItems: "center" }}>
                                <Box sx={{ width: "100%", mr: 1 }}>
                                    <LinearProgress
                                        variant="determinate"
                                        value={progress}
                                    />
                                </Box>
                                <Box sx={{ minWidth: 35 }}>
                                    <Typography
                                        variant="body2"
                                        color="text.secondary"
                                    >{`${Math.round(progress)}%`}</Typography>
                                </Box>
                            </Box>
                        </Box>
                    )}
                </Container>
                <Grid container spacing={{ xs: 2, md: 3 }}>
                    {(videos as Array<any>).map((video, index) => (
                        <Grid xs={12} sm={6} md={4} xl={2} key={index}>
                            <Thumbnail
                                id={video.id}
                                title={video.title}
                                thumbnail={video.thumbnail}
                                uploader={video.uploader}
                                upload_date={video.upload_date}
                            ></Thumbnail>
                        </Grid>
                    ))}
                </Grid>
            </Stack>
        </Layout>
    );
}
