import { Container, CircularProgress } from "@mui/material";

export const LoadingIndicator = () => {
    return (
        <Container style={{ width: "100%", textAlign: "center" }}>
            <CircularProgress />
        </Container>
    );
};

export default LoadingIndicator;
