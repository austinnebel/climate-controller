import { Container, Typography, Divider } from "@mui/material";

/** Container for a single section of a screen. */
export const AppSection = ({
    /** Section content. */
    children,
    /** Section name; is displayed above all children. */
    heading,
}: {
    children: React.ReactNode;
    heading: string;
}) => {
    return (
        <Container style={{ marginBottom: "24px", padding: 0 }}>
            <Typography variant="h4">{heading}</Typography>
            <Divider style={{ width: "100%", marginBottom: "12px" }} />
            {children}
        </Container>
    );
};

export default AppSection;
