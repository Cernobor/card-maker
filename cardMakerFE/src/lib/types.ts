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

export type CardSpec = {
    name: string,
    fluff: string,
    effect: string,
    user_id: number,
    card_type_id: number,
    in_set: boolean,
    set_name: string,
    tags: string[]
};
