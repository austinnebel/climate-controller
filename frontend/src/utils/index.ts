/**
 * Parses a Date or string object into a string of format HH:MM AM/PM
 *
 * @param {Date | string} date Parses a Date object into a string of format HH:MM AM/PM
 * @returns string
 */
export const formatDate = (date: Date | string) => {
    return new Date(date)
        .toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        })
        .replace(/\s+/g, "");
};
