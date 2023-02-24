import AppHeader from "./AppHeader";

/**
 * Main container of app content.
 * Displays the application header at the top of the screen.
 */
export const AppContainer = ({ children }: { children: React.ReactNode }) => {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: 0,
            }}
        >
            <AppHeader />

            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    padding: "12px",
                }}
            >
                {children}
            </div>
        </div>
    );
};

export default AppContainer;
