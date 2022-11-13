import create from "zustand";
import { persist } from "zustand/middleware";

export const useStore = create(
  persist(
    (set, get) => ({
      xummState: null,
      getXummState: () => get({ xummState }),
      setXummState: (xummState) => set({
        xummState: xummState
      }),
      logout: () => {
        console.log("logout");
      }
    }),
    {
      name: "xurlpay-storage", // unique name
      getStorage: () => localStorage, // (optional) by default, 'localStorage' is used
    }
  )
);

// export default useStore;

