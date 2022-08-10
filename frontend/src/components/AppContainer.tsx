import { Container } from "@mui/material";
import AppHeader from "./AppHeader";

/**
 * Main container of app content.
 * Displays the application header at the top of the screen.
 */
export const AppContainer = ({ children }: { children: React.ReactNode }) => {
    return (
        <Container
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: 0,
            }}
        >
            <AppHeader />

            <Container
                style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    padding: "12px",
                }}
            >
                {children}
            </Container>
        </Container>
    );
};

export default AppContainer;
