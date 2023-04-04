public interface IUploadFileService
{
  Task<FileModel> Upload(Stream file, String name);
  long GetMaxFileSize();
}