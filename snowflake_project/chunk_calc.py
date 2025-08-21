class ChunkCalc:
    @staticmethod
    def calculate_chunks(total_rows, min_rows_per_chunk, max_concurrency):
        """Calculate optimal number of chunks based on row count and limits."""
        if total_rows <= min_rows_per_chunk:
         # Not enough rows to split — run single-threaded
         return 1
        else:
            n = total_rows // min_rows_per_chunk
            return max(1, min(n, max_concurrency))
