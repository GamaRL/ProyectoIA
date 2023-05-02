public interface IUploadFileService
{
  Task<FileModel> Upload(Stream file, String name, AlgorithmType type);
  long GetMaxFileSize();
  public Task<List<FileModel>> GetFiles(AlgorithmType type);
  public Task<FileModel> RemoveFile(int fileId, AlgorithmType type);
  public Task<FileContentModel> GetFileContent(int fileId, AlgorithmType type);
  public string GetFileUrl(int fileId, AlgorithmType type);
}