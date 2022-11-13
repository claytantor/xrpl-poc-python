import create from "zustand";
import { persist, subscribeWithSelector } from "zustand/middleware";


// const useStore = create((set) => (
//     subscribeWithSelector(() => ({
//         xummState: null,
//         setXummState: (xummState) => set({
//             xummState: xummState
//         }),
//         getXummState: () => get({ xummState }),
//         logout: () => {
//         set({xummState: null});
//         window.location.reload();
//         }
//     }))
// ));


export const useStoreBasic = create((set) => (
    {
        xummState: null,
        setXummState: (xummState) => set({
            xummState: xummState
        }),
        getXummState: () => get({ xummState }),
        logout: () => {
            set({xummState: null});
            window.location.reload();
        }
    }
));

export const useStore = create(
  persist(
    (set, get) => ({
    //   isLoading: false,
    //   appDetails: {},
      xummState: null,
    //   setIsLoading: (isLoading) => set({ isLoading: isLoading }),
    //   getIsLoading: () => get({ isLoading }),
    //   getXummAppDetails: () => get({ appDetails }),
    //   setXummAppDetails: (appDetails) => set({
    //     appDetails: appDetails
    //   }),
      getXummState: () => get({ xummState }),
      setXummState: (xummState) => set({
        xummState: xummState
      }),
      logout: () => {
        console.log("logout");
        // set({xummState: null});
        // window.location.reload();
      }
    }),
    {
      name: "xurlpay-storage", // unique name
      getStorage: () => localStorage, // (optional) by default, 'localStorage' is used
    }
  )
);

