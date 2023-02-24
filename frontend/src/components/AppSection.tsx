import { Typography, Divider } from "@mui/material";

/** Container for a single section of a screen. */
export const AppSection = ({
    /** Section content. */
    children,
    /** Section name; is displayed above all children. */
    heading,
    /** Content container style. */
    style,
}: {
    children: React.ReactNode;
    heading: string;
    style?: React.CSSProperties;
}) => {
    return (
        <div style={{ marginBottom: "12px", padding: 0, width: "100%" }}>
            <Typography variant="h4" style={{ textAlign: "center" }}>
                {heading}
            </Typography>
            <Divider style={{ width: "100%", marginBottom: "12px" }} />
            <div style={style}>{children}</div>
        </div>
    );
};

export default AppSection;
