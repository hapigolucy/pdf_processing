import argparse
from pdf_image_extractor import PDFImageExtractor
from thread_pool_processor import ThreadPoolImageProcessor
from pdf_reassembler import PDFReassembler
from pdf_creator import PDFCreator


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process PDF images with multithreading.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_pdf", help="Path to the output PDF file.")
    parser.add_argument(
        "--threads", type=int, default=4, help="Number of threads in the thread pool (default: 4)."
    )
    args = parser.parse_args()

    input_pdf_path = args.input_pdf
    output_pdf_path = args.output_pdf
    num_threads = args.threads

    # Step 1: Extract images in the main thread
    extractor = PDFImageExtractor(input_pdf_path)
    extracted_data = extractor.extract_all()
    images = extracted_data["images"]
    hyperlinks = extracted_data["hyperlinks"]

    print("Extracted Hyperlinks:")
    for page_num, uri, text in hyperlinks:
        print(f"Page {page_num + 1}: {uri} (Text: '{text}')")

    # Step 2: Process images using a thread pool
    processor = ThreadPoolImageProcessor(images, num_threads)
    processed_images = processor.run()

    # Step 3: Reassemble or create a new PDF in the main thread
    reassembler = PDFReassembler(input_pdf_path, output_pdf_path)
    reassembler.add_images_back_to_pdf(processed_images)

    print("PDF processing completed!")


if __name__ == "__main__":
    main()
