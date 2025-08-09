def generate_contact_numbers(student_id: str):
    """
    Generate a unique pager and fax number based on a student ID.
    The numbers follow a fixed prefix and embed the student ID digits.
    """

    student_id = ''.join(filter(str.isdigit, student_id))

    while len(student_id) < 8:
        student_id += student_id

    digits = student_id[:8]

    pager_prefix = "5"
    fax_prefix = "5"

    pager = f"{pager_prefix}{digits[0]}{digits[1]}-{digits[2]}{digits[3]}{digits[4]}-{digits[5]}{digits[6]}{digits[7]}{digits[0]}"
    fax = f"({fax_prefix}{digits[0]}{digits[1]}) {digits[2]}{digits[3]}{digits[4]}-{digits[5]}{digits[6]}{digits[7]}{digits[0]}"

    return pager, fax


