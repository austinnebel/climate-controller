# Climate Controller Frontend

This is the frontend of the climate controller. The frontend is built with React and TypeScript.

To run this project in a docker container, run the following in this directory:

```bash
docker build -t climate-controller-frontend .

docker run -p 3000:3000 climate-controller-frontend
```

> **NOTE**
>
> The above command will not be able to communicate with the other containers unless they are on the same virtual network. This is done automatically by `docker compose`.

## Requirements

-   Node.js v11
    -   Node v11 was the last Node version supported on armv6l devices (such as the RPi Zero). This can be easily installed using a version manager such as `nvm`.
-   `npm`
    -   Will be packaged with Node.

## React Scripts

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run serve`

Serves the built application in production mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will NOT reload if you make edits. You will need to re-build the project and re-run this command each time changes are made.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.
