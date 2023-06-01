public class HeaderSelection
{
  public object Header { get; set; }
  public bool IsSelected { get; set; }

  public HeaderSelection(object Header)
  {
    this.Header = Header;
    this.IsSelected = true;
  }

  public HeaderSelection(HeaderSelection selection)
  {
    this.Header = selection.Header;
    this.IsSelected = false;
  }
}