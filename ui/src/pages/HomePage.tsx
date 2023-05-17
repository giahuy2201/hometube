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
} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2
import Thumbnail from "../components/Thumbnail";
import axios from "axios";

export default function HomePage() {
    const [url, setURL] = React.useState("");
    const [preset, setPreset] = React.useState("bestvideo");

    const updateURL = (event: React.ChangeEvent<HTMLInputElement>) => {
        setURL(event.target.value);
    };

    const updatePreset = (event: SelectChangeEvent) => {
        setPreset(event.target.value);
    };

    const submitRequest = async () => {
        const result = await axios.post("http://localhost:8000/add", {
            url: url,
            preset: preset
        });
        console.log(result);
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
                                <MenuItem value={'bestvideo'}>bestvideo</MenuItem>
                                <MenuItem value={'bestaudio'}>bestaudio</MenuItem>
                                <MenuItem value={'new'}>
                                    <em>New preset</em>
                                </MenuItem>
                            </Select>
                            <Button variant="contained" onClick={submitRequest}>
                                Download
                            </Button>
                        </Stack>
                    </Stack>
                </Container>
                <Grid container spacing={{ xs: 2, md: 3 }}>
                    {Array.from(Array(20)).map((_, index) => (
                        <Grid xs={12} sm={6} md={4} xl={2} key={index}>
                            <Thumbnail></Thumbnail>
                        </Grid>
                    ))}
                </Grid>
            </Stack>
        </Layout>
    );
}
