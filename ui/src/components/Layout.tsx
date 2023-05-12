import React, { ReactNode } from "react";
import { Outlet } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import NavBar from "./NavBar";
import { CssBaseline } from "@mui/material";

type LayoutProps = {
    children: ReactNode;
};

export default function Layout(props: LayoutProps) {
    return (
        <div>
            <CssBaseline />
            <NavBar />
            {props.children}
        </div>
    );
}
