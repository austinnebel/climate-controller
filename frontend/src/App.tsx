import { MainScreen } from "screens/main/MainScreen";
import { ThemeProvider } from "theme";

export const App = () => {
    return (
        <ThemeProvider>
            <MainScreen />
        </ThemeProvider>
    );
};

export default App;
