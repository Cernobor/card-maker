/**
 * Functions used for error handling in typescript request functions.
 */
import type { ErrorWithMessage } from './interfaces';

function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
    /**
     * Determine if error contains message.
     * 
     * @param error - error object of unknown type
     * @returns if error is error with message
     */
	return (
		typeof error === 'object' &&
		error !== null &&
		'message' in error &&
		typeof (error as Record<string, unknown>).message === 'string'
	)
}


function toErrorWithMessage(maybeError: unknown): ErrorWithMessage {
    /**
     * Cast error to error with message
     * 
     * @param maybeError - error object of unknown type
     * @returns error with message
     */
	if (isErrorWithMessage(maybeError)) return maybeError

	try {
		return new Error(JSON.stringify(maybeError))
	} catch {
		// fallback in case there's an error stringifying the maybeError
		// like with circular references for example.
		return new Error(String(maybeError))
	}
}


export function getErrorMessage(error: unknown): string {
    /**
     * Get message from error.
     * 
     * @param error - error object of unknown type
     * @returns error message
     */
	return toErrorWithMessage(error).message
}