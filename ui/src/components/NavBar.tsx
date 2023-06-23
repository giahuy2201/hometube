import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import AccountCircle from "@mui/icons-material/AccountCircle";
import SettingsRoundedIcon from "@mui/icons-material/SettingsRounded";
import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import SearchModal from "../pages/SearchModal";

export default function NavBar() {
    const [auth, setAuth] = React.useState(true);
    const [searchModalOpen, setSearchModalOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const openSearchModal = () => {
        setSearchModalOpen(true);
    };

    const closeSearchModal = () => {
        setSearchModalOpen(false);
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ flexGrow: 1 }}
                    >
                        mytube
                    </Typography>
                    <IconButton
                        size="large"
                        color="inherit"
                        onClick={openSearchModal}
                    >
                        <SearchRoundedIcon />
                    </IconButton>
                    {auth && (
                        <div>
                            <IconButton
                                size="large"
                                aria-label="account of current user"
                                aria-controls="menu-appbar"
                                aria-haspopup="true"
                                onClick={handleMenu}
                                color="inherit"
                            >
                                <AccountCircle />
                            </IconButton>
                            <Menu
                                id="menu-appbar"
                                anchorEl={anchorEl}
                                anchorOrigin={{
                                    vertical: "top",
                                    horizontal: "right",
                                }}
                                keepMounted
                                transformOrigin={{
                                    vertical: "top",
                                    horizontal: "right",
                                }}
                                open={Boolean(anchorEl)}
                                onClose={handleClose}
                            >
                                <MenuItem onClick={handleClose}>
                                    Profile
                                </MenuItem>
                                <MenuItem onClick={handleClose}>
                                    Logout
                                </MenuItem>
                            </Menu>
                        </div>
                    )}
                </Toolbar>
            </AppBar>
            <SearchModal
                open={searchModalOpen}
                handleClose={closeSearchModal}
            ></SearchModal>
        </Box>
    );
}
