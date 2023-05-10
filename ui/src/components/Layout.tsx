import React, { ReactNode } from 'react';
import { Outlet } from "react-router-dom";
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';

type LayoutProps = {
    children: ReactNode
}

export default function Layout(props: LayoutProps) {
    return (
        <Container>
            <Box>
                {props.children}
            </Box>
        </Container>
    )
}