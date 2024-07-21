export type Author = {
    name: string;
    id: number;
};

export type CardType = {
    name: string;
    id: number;
};

export type Tag = {
    name: string;
    value: string;
    id: number;
}

export type ErrorWithMessage = {
    message: string;
}

export type User = {
    username: string;
    password: string;
}