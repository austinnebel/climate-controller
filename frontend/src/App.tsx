import { AppContainer } from "components";
import { MainScreen } from "screens/main/MainScreen";
import { ThemeProvider } from "theme";

export const App = () => {
    return (
        <ThemeProvider>
            <AppContainer>
                <MainScreen />
            </AppContainer>
        </ThemeProvider>
    );
};

export default App;
