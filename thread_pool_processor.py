from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from image_processor import ImageProcessor


class ThreadPoolImageProcessor:
    """Manages multithreaded processing of images using a thread pool."""
    def __init__(self, images, num_threads):
        self.images = images
        self.num_threads = num_threads
        self.processed_images = Queue()

    def process_image(self, page_num, img_index, img_obj, ext):
        """Process a single image."""
        print(f"Processing image {img_index} on page {page_num}...")
        modified_image = ImageProcessor.modify_image(img_obj)
        print(f"Finished processing image {img_index} on page {page_num}.")
        return page_num, img_index, modified_image, ext

    def run(self):
        """Execute image processing using a thread pool."""
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_image = {
                executor.submit(self.process_image, page_num, img_index, img_obj, ext): (page_num, img_index)
                for page_num, img_index, img_obj, ext in self.images
            }

            for future in as_completed(future_to_image):
                try:
                    result = future.result()
                    self.processed_images.put(result)
                except Exception as e:
                    print(f"Error processing image {future_to_image[future]}: {e}")

        # Collect all processed images from the queue
        return list(self.processed_images.queue)
