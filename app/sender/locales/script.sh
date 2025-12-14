LOCALES_DIR="${PWD}/app/sender/locales"

for LANG in $(ls "${LOCALES_DIR}" | grep -E '^([a-z]{2})$'); do
    MO_FILE="${LOCALES_DIR}/${LANG}/LC_MESSAGES/messages.mo"
    PO_FILE="${LOCALES_DIR}/${LANG}/LC_MESSAGES/messages.po"

    if [ ! -f "$PO_FILE" ]; then
        continue
    fi

    echo "Build translations for lang ${LANG}"
    msgfmt -c -v -o "$MO_FILE" "$PO_FILE"
done

echo "Translations build succesfully"
exit 0