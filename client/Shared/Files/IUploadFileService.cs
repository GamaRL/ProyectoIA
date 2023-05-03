public interface IUploadFileService
{
  Task<FileModel> Upload(Stream file, String name, AlgorithmType type);
  long GetMaxFileSize();
  Task<List<FileModel>> GetFiles(AlgorithmType type);
  Task<FileModel> RemoveFile(int fileId, AlgorithmType type);
  Task<FileContentModel> GetFileContent(int fileId, AlgorithmType type);
  string GetFileUrl(int fileId, AlgorithmType type);
  Task<List<object>> GetFileHeaders(int fileId, bool contains_headers, AlgorithmType type);
}