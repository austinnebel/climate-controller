import { createTheme, ThemeProvider as MUIThemeProvider } from "@mui/material";
import React from "react";

const theme = createTheme({
    palette: {
        primary: {
            main: "#e43124",
        },
        secondary: {
            main: "#eb3124",
        },
        text: {
            primary: "#fff",
            secondary: "#e43124",
        },
    },
    typography: {
        fontFamily: "Montserrat",
        allVariants: {
            color: "gray",
        },
    },
    shape: {
        borderRadius: 4,
    },
});

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
    return <MUIThemeProvider theme={theme}> {children} </MUIThemeProvider>;
};
