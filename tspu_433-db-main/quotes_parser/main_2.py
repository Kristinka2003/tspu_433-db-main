from quotes_parser.db_utils import get_by_tags, get_by_authors




def main():
    print("Цитаты по тегу 'life':")
    quotes = get_by_tags(["life"])
    for text, author in quotes:
        print(f"\"{text}\" — {author}")

    print("\nЦитаты по автору 'Albert Einstein':")
    quotes = get_by_authors(["Albert Einstein"])
    for text, author in quotes:
        print(f"\"{text}\" — {author}")

if __name__ == "__main__":
    main()
