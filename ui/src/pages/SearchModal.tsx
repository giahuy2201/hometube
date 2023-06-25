import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { styled, alpha } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import axios from "axios";
import { Grid, Stack } from "@mui/material";
import Thumbnail from "../components/Thumbnail";

const style = {
    position: "absolute" as "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: "50%",
    // height: "50%",
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
};

type SearchModalProps = {
    open: boolean;
    handleClose: () => void;
};

export default function SearchModal(props: SearchModalProps) {
    const [videos, setVideos] = React.useState<any>([]);

    const sendSearchRequest = (event: React.ChangeEvent<HTMLInputElement>) => {
        let term = event.target.value;
        if (term != "") {
            axios
                .get("http://localhost:8000/videos?term=" + term)
                .then((res) => {
                    console.log(res["data"]);
                    setVideos(res["data"]);
                });
        }
    };

    return (
        <Modal
            open={props.open}
            onClose={props.handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
                <Stack
                    direction="column"
                    spacing={2}
                    justifyContent="center"
                    alignItems="stretch"
                    flexWrap="nowrap"
                >
                    <Search>
                        <SearchIconWrapper>
                            <SearchIcon />
                        </SearchIconWrapper>
                        <StyledInputBase
                            placeholder="Search…"
                            inputProps={{ "aria-label": "search" }}
                            onChange={sendSearchRequest}
                        />
                    </Search>
                    <Grid container spacing={{ xs: 2, md: 3 }}>
                        {(videos as Array<any>).map((video, index) => (
                            <Grid xs={12} sm={6} md={4} xl={2} key={index}>
                                <Thumbnail
                                    variant='list'
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
            </Box>
        </Modal>
    );
}

const Search = styled("div")(({ theme }) => ({
    position: "relative",
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    "&:hover": {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
        marginLeft: theme.spacing(1),
        width: "auto",
    },
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: "inherit",
    "& .MuiInputBase-input": {
        padding: theme.spacing(1, 1, 1, 0),
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create("width"),
        width: "100%",
        [theme.breakpoints.up("sm")]: {
            width: "12ch",
            "&:focus": {
                width: "20ch",
            },
        },
    },
}));
