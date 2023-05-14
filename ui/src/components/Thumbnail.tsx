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
} from "@mui/material";
import { ExpandMore } from "@mui/icons-material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import DownloadRoundedIcon from '@mui/icons-material/DownloadRounded';
import { red } from "@mui/material/colors";

type ThumbnailProps = {};

export default function Thumbnail(props: ThumbnailProps) {
    return (
        <Card variant="outlined">
            <CardMedia
                component="img"
                image="https://mui.com/static/images/cards/contemplative-reptile.jpg"
                alt="Paella dish"
            />
            <CardHeader
                avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
                        R
                    </Avatar>
                }
                action={
                    <IconButton aria-label="download">
                        <DownloadRoundedIcon />
                    </IconButton>
                }
                title="Shrimp and Chorizo Paella"
                subheader="September 14, 2016"
            />
        </Card>
    );
}
