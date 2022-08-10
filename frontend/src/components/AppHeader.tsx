import { DeviceThermostat } from "@mui/icons-material";
import { Container, useTheme } from "@mui/material";

export const AppHeader = () => {
    const theme = useTheme();

    return (
        <Container
            sx={{ borderBottom: `1px solid ${theme.palette.primary.main}` }}
            style={{
                width: "100%",
                height: "auto",
                padding: "12px",
                margin: 0,
                display: "flex",
                flexDirection: "column",
                alignContent: "center",
                justifyContent: "center",
            }}
        >
            <DeviceThermostat
                height={"4em"}
                color="primary"
                style={{ width: "auto" }}
            />
        </Container>
    );
};

export default AppHeader;
