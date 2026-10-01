import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


MAJOR_SECTION_PATTERN = re.compile(
    r"^\d+\.\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 /,&()_-]+$"
)
SUBSECTION_PATTERN = re.compile(r"^\d+\.\d+\s+\S.+$")


def _is_section_title(line: str) -> bool:
    return bool(
        MAJOR_SECTION_PATTERN.match(line)
        or SUBSECTION_PATTERN.match(line)
    )


def _split_into_sections(document: Document) -> list[Document]:
    sections: list[Document] = []
    current_title = "Introducao"
    current_lines: list[str] = []

    def append_current_section() -> None:
        content = "\n".join(current_lines).strip()
        if not content:
            return

        sections.append(
            Document(
                page_content=content,
                metadata={
                    **document.metadata,
                    "section": current_title,
                },
            )
        )

    for raw_line in document.page_content.splitlines():
        line = raw_line.strip()

        if not line or set(line) == {"="}:
            if current_lines and current_lines[-1] != "":
                current_lines.append("")
            continue

        if _is_section_title(line):
            append_current_section()
            current_title = line
            current_lines = [line]
            continue

        current_lines.append(line)

    append_current_section()
    return sections


def split_documents_by_section(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    section_documents: list[Document] = []

    for document in documents:
        section_documents.extend(_split_into_sections(document))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(section_documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

    return chunks
