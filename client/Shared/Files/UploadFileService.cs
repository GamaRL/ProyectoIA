using System.Net.Http.Headers;
using System.Net.Http.Json;

public class UploadFileService : IUploadFileService
{
  private readonly HttpClient _http;

  public UploadFileService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<FileModel> Upload(Stream file, String fileName)
  {
    MultipartFormDataContent content = new();
    try
    {
      var fileContent = new StreamContent(file);

      fileContent.Headers.ContentType = new MediaTypeHeaderValue("text/csv");

      content.Add(
        content: fileContent,
        name: "file",
        fileName: fileName
      );

    }
    catch (Exception ex)
    {
      Console.WriteLine(ex.ToString());
    }

    var response = await _http.PostAsync("/1/files/", content);

    return await response.Content.ReadFromJsonAsync<FileModel>();
  }

  public long GetMaxFileSize()
  {
    return 20 * 1024L * 1024L;
  }
}