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

      userCurrency: "USD",
      getUserCurrency: () => get({ userCurrency }),
      setUserCurrency: (userCurrency) => set({
        userCurrency: userCurrency
      }),

      //========== ITEM CART ====================================
      paymentItemCart: [],
      emptyCart: () => set({ paymentItemCart: [] }),
      getCartSize: () => {
        return lodash.sumBy(get().paymentItemCart, "qty");
      },
      removePaymentItemFromCart: (paymentItem) => {
        const isItemInCart = get().paymentItemCart.find(
          (paymentItemInCart) => paymentItemInCart.id === paymentItem.id
        );
        if (isItemInCart && isItemInCart.qty > 1) {
          set((state) => ({
            ...state,
            paymentItemCart: state.paymentItemCart.map((item) => {
              console.log("", item.id, paymentItem.id);
              return item.id === paymentItem.id
                ? {
                    ...item,
                    qty:
                      typeof item?.qty === "number" ? item.qty - 1 : item.qty,
                  }
                : item;
            }),
          }));
        } else {
          let cartCopy = [...get().paymentItemCart];
          lodash.remove(cartCopy, (item) => item.id === paymentItem.id);
          set((state) => ({
            ...state,
            paymentItemCart: cartCopy,
          }));
        }
      },
      addPaymentItemToCart: (paymentItem) => {
        const isItemInCart = get().paymentItemCart.find(
          (paymentItemInCart) => paymentItemInCart.id === paymentItem.id
        );
        if (isItemInCart) {
          set((state) => ({
            ...state,
            paymentItemCart: state.paymentItemCart.map((item) => {
              console.log("", item.id, paymentItem.id);
              return item.id === paymentItem.id
                ? {
                    ...item,
                    qty:
                      typeof item?.qty === "number" ? item.qty + 1 : item.qty,
                  }
                : item;
            }),
          }));
        } else {
          // add if doesnt exist
          set((state) => ({
            ...state,
            paymentItemCart: [
              ...state.paymentItemCart,
              {
                ...paymentItem,
                qty: 1,
              },
            ],
          }));
        }
      },
      //=========================================================================
    }),
    {
      name: "xurlpay-storage", // unique name
      getStorage: () => localStorage, // (optional) by default, 'localStorage' is used
    }
  )
);


const useBearStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))


