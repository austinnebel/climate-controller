import { DeviceThermostat } from "@mui/icons-material";
import { Container, useTheme } from "@mui/material";

export const AppHeader = () => {
    const theme = useTheme();

    return (
        <div
            style={{
                width: "100%",
                height: "auto",
                padding: "12px",
                margin: 0,
                display: "flex",
                justifyContent: "center",
                borderBottom: `1px solid ${theme.palette.primary.main}`,
            }}
        >
            <DeviceThermostat
                height={"4em"}
                color="primary"
                style={{ width: "auto" }}
            />
        </div>
    );
};

export default AppHeader;
