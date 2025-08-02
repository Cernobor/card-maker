/**
 * Interfaces used for type declaration and for requests ti API.
 */

export interface Tag {
	/**
	 * Interface used for work with card tags.
	 */
	name: string;
	description?: string | null;
}

export interface CardBase {
	/**
	 * Base interface for all card interfaces.
	 * Used also for '/api/cards' PUT method.
	 */
	name: string;
	fluff: string | null;
	effect: string | null;
	in_set: boolean;
	set_name: string | null;
	tags: Tag[];
	size: string | null;
}

export interface CardCreate extends CardBase {
	/**
	 * Interface for card creattion on '/api/cards' POST.
	 * Also used as base interface for CardGet.
	 */
	user_id: number | null;
	card_type_id: number;
}

export interface CardGet extends CardCreate {
	/**
	 * Interface for card creattion on '/api/cards/{id}' PUT.
	 */
	id: number;
}

interface UserBase {
	/**
	 * Base interface used for all user interfaces;
	 */
	username: string;
}

export interface UserLogin extends UserBase {
	/**
	 * Interface used for '/api/users/me' POST.
	 */
	password: string;
}

export interface UserCreate extends UserLogin {
	/**
	 * Interface used for '/api/users' POST.
	 */
	api_key: string;
}

export interface UserPublic extends UserBase {
	/**
	 * Interface used for '/api/users' GET.
	 * Also used for getting 'user_id' in other POST methods.
	 */
	id: number;
}

export interface JWTToken {
	/**
	 * Definition of response body in /users/me POST
	 */
	access_token: string;
	token_type: string;
	user_id: number;
}

export function isUserPublic(instance: unknown): instance is UserPublic {
	/**
	 * Determine if variable is of type UserPublic.
	 *
	 * @param instance - variable of unknown type
	 * @returns predicate if variable is of type UserPublic
	 */
	if (typeof instance !== 'object' || instance === null) {
		return false;
	}

	const obj = instance as Record<string, unknown>;

	return typeof obj.username === 'string' && typeof obj.id === 'number';
}

export interface CardType {
	/**
	 * Interface used for '/api/card-types' GET.
	 * Also used for getting 'card_type_id' in other POST methods.
	 */
	id: number;
	name: string;
}

export interface ErrorWithMessage {
	/**
	 * Interface used for define error containing message.
	 */
	message: string;
}

export function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
	/**
	 * Determine if error contains message.
	 *
	 * @param error - error object of unknown type
	 * @returns predicate if error is error with message
	 */
	return (
		typeof error === 'object' &&
		error !== null &&
		'message' in error &&
		typeof (error as Record<string, unknown>).message === 'string'
	);
}

export type Mode = 'create' | 'update' | 'preview';

export const cardTypeClass = {
	/**
	 * Enum used to determine which
	 * css class to choose in Card component
	 */
	'Magický předmět': 'card-magical-item',
	'Volný aspekt': 'card-free-aspect',
	'Lokace-small': 'card-location-small',
	'Lokace-medium': 'card-location-medium',
	'Lokace-large': 'card-location-large',
	'Zaříkadlo': 'card-spell',
	'Recept': 'card-recipe',

} as const;

export type CardTypeKey = keyof typeof cardTypeClass;
export type CardTypeClass = (typeof cardTypeClass)[CardTypeKey];

export type Format = undefined | "pdf" | "png";

export const Color = {
	"red": "#990000",
	"green": "#336600",
	"blue": "#006699"
} as const;

export type ColorType = (typeof Color)[keyof typeof Color]

export interface FlashMessage {
	id: number
	message: string
	color: ColorType
}