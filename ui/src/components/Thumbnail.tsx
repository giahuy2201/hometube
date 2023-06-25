import React, { ReactNode } from "react";
import { Outlet } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import NavBar from "./NavBar";
import {
    Avatar,
    Card,
    CardActions,
    CardContent,
    CardHeader,
    CardMedia,
    Collapse,
    CssBaseline,
    IconButton,
    useTheme,
} from "@mui/material";
import { ExpandMore } from "@mui/icons-material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import SkipPreviousIcon from "@mui/icons-material/SkipPrevious";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { red } from "@mui/material/colors";
import axios from "axios";

type ThumbnailProps = {
    id: string;
    title: string;
    thumbnail: string;
    uploader: string;
    upload_date: string;
    variant: string;
};

export default function Thumbnail(props: ThumbnailProps) {
    const theme = useTheme();

    function downloadFile() {
        window.open("http://localhost:8000/download?id=" + props.id);
    }

    return (
        <>
            {props.variant && props.variant == "list" ? (
                <Card
                    variant="outlined"
                    sx={{ display: "flex", width: "100%" }}
                >
                    <CardMedia
                        component="img"
                        image={props.thumbnail}
                        sx={{
                            objectFit: "contain",
                            flex: 0,
                            maxHeight: "200px",
                        }}
                    />

                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "flex-start",
                        }}
                    >
                        <CardContent sx={{ flex: "1 0 auto" }}>
                            <Typography component="div" variant="h5">
                                {props.title}
                            </Typography>
                            <Typography
                                variant="subtitle1"
                                color="text.secondary"
                                component="div"
                            >
                                {props.uploader}
                            </Typography>
                            <Typography variant="subtitle2" component="div">
                                {props.upload_date}
                            </Typography>
                        </CardContent>
                        <IconButton
                            onClick={downloadFile}
                            aria-label="download"
                        >
                            <DownloadRoundedIcon />
                        </IconButton>
                    </Box>
                </Card>
            ) : (
                <Card variant="outlined">
                    <CardMedia component="img" image={props.thumbnail} />
                    <CardHeader
                        avatar={
                            <Avatar sx={{ bgcolor: red[500] }}>
                                {props.uploader}
                            </Avatar>
                        }
                        action={
                            <IconButton
                                onClick={downloadFile}
                                aria-label="download"
                            >
                                <DownloadRoundedIcon />
                            </IconButton>
                        }
                        title={props.title}
                        subheader={props.upload_date}
                    />
                </Card>
            )}
        </>
    );
}
