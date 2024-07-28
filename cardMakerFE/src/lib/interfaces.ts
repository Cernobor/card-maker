/**
 * Interfaces used for type declaration and for requests ti API.
 */

export interface Tag {
	/**
	 * Interface used for work with card tags.
	 */
	name: string;
	description: string | null;
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
}

export interface CardCreate extends CardBase {
	/**
	 * Interface for card creattion on '/api/cards' POST.
	 * Also used as base interface for CardGet.
	 */
	user_id: number;
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

export interface UserCreate extends UserBase {
	/**
	 * Interface used for '/api/users' POST.
	 */
	password: string;
}

export interface UserPublic extends UserBase {
	/**
	 * Interface used for '/api/users' GET.
	 * Also used for getting 'user_id' in other POST methods.
	 */
	id: number;
}

export function isUserPublic(instance: unknown): instance is UserPublic {
	/**
	 * Determine if variable is of type UserPublic.
	 *
	 * @param instance - variable of unknown type
	 * @returns predicate if variable is of type UsrePublic
	 */
	return (
		typeof instance === 'object' &&
		instance !== null &&
		'message' in instance &&
		typeof (instance as Record<string, unknown>).username === 'string'
	);
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
